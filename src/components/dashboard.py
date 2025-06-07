import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
from ..database.db_manager import DatabaseManager

class Dashboard:
    def __init__(self):
        self.db = DatabaseManager()
        
    def _create_radar_chart(self, performance_data: Dict[str, float]):
        categories = ['Attention', 'Eye Contact', 'Speech Clarity',
                     'Confidence', 'Body Language']
        values = [
            performance_data['attention'],
            performance_data['eye_contact'],
            performance_data['speech_clarity'],
            performance_data['confidence'],
            performance_data['body_language']
        ]
        
        fig = go.Figure(data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Current Performance'
            )
        ])
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False
        )
        
        return fig
    
    def _create_trend_chart(self, history: List[Dict[str, Any]]):
        df = pd.DataFrame(history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        fig = go.Figure()
        metrics = ['attention_score', 'eye_contact_score', 'speech_clarity_score',
                  'confidence_score', 'body_language_score']
        
        for metric in metrics:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df[metric],
                name=metric.replace('_score', '').title(),
                mode='lines+markers'
            ))
        
        fig.update_layout(
            title='Performance Trends',
            xaxis_title='Interview Date',
            yaxis_title='Score',
            yaxis=dict(range=[0, 1])
        )
        
        return fig
        
    def show_performance_metrics(self, user_id):
        st.title("Interview Performance Dashboard")
        
        # Get performance data
        performance_summary = self.db.get_performance_summary(user_id)
        performance_history = self.db.get_performance_history(user_id, limit=10)
        stats = self.db.get_user_statistics(user_id)
        
        # Display overall statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Interviews", stats['total_interviews'])
        with col2:
            st.metric("Average Score", f"{stats['avg_score']:.1%}")
        with col3:
            st.metric("Practice Time", f"{stats['total_time']:.1f} hours")
            
        # Display radar chart for overall performance
        st.subheader("Performance Overview")
        if performance_summary:
            radar_chart = self._create_radar_chart(performance_summary)
            st.plotly_chart(radar_chart, use_container_width=True)
        else:
            st.info("Complete more interviews to see your performance overview!")
            
        # Display trend chart
        st.subheader("Performance Trends")
        if performance_history:
            trend_chart = self._create_trend_chart(performance_history)
            st.plotly_chart(trend_chart, use_container_width=True)
        else:
            st.info("Complete more interviews to see your performance trends!")
            
        # Show recommendations
        self.show_recommendations(user_id)
        
    def show_statistics(self, user_id):
        st.subheader("Detailed Statistics")
        
        # Get detailed interview data
        interviews = self.db.get_user_interviews(user_id)
        if not interviews:
            st.info("No interview data available yet. Complete some interviews to see your statistics!")
            return
            
        df = pd.DataFrame(interviews)
        
        # Category performance
        st.write("### Performance by Category")
        category_scores = df.groupby('category')['score'].agg(['mean', 'count']).round(3)
        category_scores.columns = ['Average Score', 'Number of Interviews']
        st.dataframe(category_scores)
        
        # Progress over time
        st.write("### Progress Over Time")
        fig_progress = px.line(df, 
                             x='date', 
                             y='score',
                             title='Score Progression',
                             labels={'date': 'Interview Date', 'score': 'Score'})
        st.plotly_chart(fig_progress)
        
        # Recent activity
        st.write("### Recent Activity")
        recent = df.nlargest(5, 'date')[['date', 'job_role', 'question', 'score']]
        for _, row in recent.iterrows():
            with st.expander(f"{row['date'][:10]} - {row['job_role']}"):
                st.write(f"**Question:** {row['question']}")
                st.write(f"**Score:** {row['score']:.2%}")
    
    def show_recommendations(self, user_id):
        st.subheader("Improvement Recommendations")
        
        performance_summary = self.db.get_performance_summary(user_id)
        if not performance_summary:
            st.info("Complete more interviews to receive personalized recommendations!")
            return
            
        recommendations = []
        
        if performance_summary['attention'] < 0.7:
            recommendations.append("""
            - **Attention Focus:**
              - Practice maintaining focus during longer conversations
              - Take short breaks between practice sessions
              - Minimize distractions in your environment
            """)
            
        if performance_summary['eye_contact'] < 0.7:
            recommendations.append("""
            - **Eye Contact:**
              - Look directly at the camera when speaking
              - Practice with a friend via video call
              - Set up your camera at eye level
            """)
            
        if performance_summary['speech_clarity'] < 0.7:
            recommendations.append("""
            - **Speech Clarity:**
              - Practice speaking slowly and clearly
              - Record yourself and listen for areas of improvement
              - Use tongue twisters for articulation practice
            """)
            
        if performance_summary['confidence'] < 0.7:
            recommendations.append("""
            - **Confidence:**
              - Prepare and practice responses to common questions
              - Use positive body language
              - Focus on your achievements and strengths
            """)
            
        if performance_summary['body_language'] < 0.7:
            recommendations.append("""
            - **Body Language:**
              - Maintain good posture
              - Use appropriate hand gestures
              - Practice in front of a mirror
            """)
            
        if not recommendations:
            st.write("Great job! Your performance is strong across all areas. Keep practicing to maintain your skills.")
        else:
            for recommendation in recommendations:
                st.markdown(recommendation)
