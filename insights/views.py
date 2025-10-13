from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SpendingInsight
from .utils import generate_insights_for_user


@login_required
def insights_dashboard(request):
    """
    Display all insights for the logged-in user.
    """
    # Generate fresh insights
    generate_insights_for_user(request.user)
    
    # Get all insights
    insights = SpendingInsight.objects.filter(user=request.user)
    
    # Separate by type
    predictions = insights.filter(insight_type='prediction')
    alerts = insights.filter(insight_type='alert')
    recommendations = insights.filter(insight_type='recommendation')
    tips = insights.filter(insight_type='tip')
    
    context = {
        'predictions': predictions,
        'alerts': alerts,
        'recommendations': recommendations,
        'tips': tips,
        'total_insights': insights.count(),
        'unread_count': insights.filter(is_read=False).count(),
    }
    
    return render(request, 'insights/insights_dashboard.html', context)


@login_required
def mark_insight_read(request, pk):
    """
    Mark an insight as read.
    """
    insight = get_object_or_404(SpendingInsight, pk=pk, user=request.user)
    insight.is_read = True
    insight.save()
    
    return redirect('insights_dashboard')


@login_required
def delete_insight(request, pk):
    """
    Delete an insight.
    """
    insight = get_object_or_404(SpendingInsight, pk=pk, user=request.user)
    insight.delete()
    messages.success(request, 'Insight deleted successfully.')
    
    return redirect('insights_dashboard')
