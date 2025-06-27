#!/usr/bin/env python3
"""
AI Real Estate Investment Chatbot
RAG-powered conversational AI for property investment consultation
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import openai
from dataclasses import dataclass

@dataclass
class ChatContext:
    client_id: str
    session_id: str
    preferences: Dict
    conversation_history: List[Dict]
    current_focus: Optional[str] = None

class RealEstateRAGChatbot:
    """RAG-powered Real Estate Investment Chatbot"""
    
    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key
        self.property_data = self._load_property_database()
        self.market_knowledge = self._load_market_intelligence()
        self.conversation_contexts = {}
        
    def _load_property_database(self) -> List[Dict]:
        """Load latest property analysis data"""
        data_dir = "../data"
        analysis_dir = "../reports"
        
        # Load raw property data
        try:
            data_files = [f for f in os.listdir(data_dir) if f.startswith("bayut_properties_")]
            if data_files:
                latest_file = sorted(data_files, reverse=True)[0]
                with open(os.path.join(data_dir, latest_file), 'r') as f:
                    raw_properties = json.load(f)
            else:
                raw_properties = []
        except:
            raw_properties = []
            
        # Load analysis results
        try:
            analysis_files = [f for f in os.listdir(analysis_dir) if f.startswith("investment_analysis_")]
            if analysis_files:
                latest_analysis = sorted(analysis_files, reverse=True)[0]
                with open(os.path.join(analysis_dir, latest_analysis), 'r') as f:
                    analysis_data = json.load(f)
                analyzed_properties = analysis_data.get('opportunities', [])
            else:
                analyzed_properties = []
        except:
            analyzed_properties = []
            
        print(f"📊 Loaded {len(analyzed_properties)} analyzed properties for chatbot")
        return analyzed_properties
    
    def _load_market_intelligence(self) -> Dict:
        """Load market knowledge base"""
        return {
            'market_trends': {
                'Dubai': {
                    'growth_rate': 8.5,
                    'trend': 'increasing',
                    'drivers': ['Expo legacy', 'Golden visa program', 'Economic diversification'],
                    'outlook': 'positive'
                },
                'Abu_Dhabi': {
                    'growth_rate': 6.2,
                    'trend': 'stable',
                    'drivers': ['Government investments', 'Tourism growth', 'Cultural development'],
                    'outlook': 'stable'
                },
                'Riyadh': {
                    'growth_rate': 12.3,
                    'trend': 'rapidly_increasing',
                    'drivers': ['Vision 2030', 'NEOM project', 'Economic transformation'],
                    'outlook': 'very_positive'
                }
            },
            'investment_advice': {
                'beginner': [
                    'Start with established areas like Downtown Dubai or Dubai Marina',
                    'Consider apartments over villas for easier liquidity',
                    'Budget 20-30% above asking price for fees and furnishing',
                    'Research rental yields in your target area'
                ],
                'experienced': [
                    'Diversify across property types and locations',
                    'Consider off-plan developments for capital appreciation',
                    'Monitor government policy impacts on property values',
                    'Leverage financing options for portfolio expansion'
                ],
                'enterprise': [
                    'Focus on commercial properties and large residential projects',
                    'Consider REITs for passive income generation',
                    'Analyze macro-economic indicators for timing',
                    'Establish relationships with local developers and agents'
                ]
            }
        }
    
    def start_conversation(self, client_id: str, client_preferences: Dict = None) -> str:
        """Initialize new conversation session"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        context = ChatContext(
            client_id=client_id,
            session_id=session_id,
            preferences=client_preferences or {},
            conversation_history=[]
        )
        
        self.conversation_contexts[session_id] = context
        
        welcome_message = self._generate_welcome_message(context)
        self._add_to_history(session_id, "assistant", welcome_message)
        
        return f"Session ID: {session_id}\n\n{welcome_message}"
    
    def _generate_welcome_message(self, context: ChatContext) -> str:
        """Generate personalized welcome message"""
        budget = context.preferences.get('budget_range', [800000, 2000000])
        areas = context.preferences.get('preferred_areas', ['Dubai Marina', 'Downtown Dubai'])
        
        return f"""🏠 Welcome to your AI Real Estate Investment Consultant!

I'm your personal property investment advisor, powered by analysis of 500+ Dubai properties and comprehensive market intelligence.

I can help you with:
🎯 Find investment opportunities in your budget (AED {budget[0]:,} - {budget[1]:,})
📊 Analyze specific properties and their ROI potential
📈 Market trends and timing advice
💡 Investment strategies tailored to your goals
🏢 Area comparisons and recommendations

Your preferences: {', '.join(areas)} | Budget: AED {budget[0]:,} - {budget[1]:,}

What would you like to explore today? Try asking:
• "What are the best investment opportunities under 1.5M AED?"
• "Should I invest in Dubai Marina or Downtown Dubai?"
• "What's the ROI potential for Palm Jumeirah villas?"
• "Tell me about the current market trends in Dubai"
"""
    
    def chat(self, session_id: str, user_message: str) -> str:
        """Process user message and generate response"""
        if session_id not in self.conversation_contexts:
            return "❌ Session not found. Please start a new conversation."
        
        context = self.conversation_contexts[session_id]
        self._add_to_history(session_id, "user", user_message)
        
        # Analyze user intent and extract relevant information
        intent = self._analyze_intent(user_message)
        relevant_data = self._retrieve_relevant_information(user_message, context)
        
        # Generate AI response using RAG
        response = self._generate_response(user_message, intent, relevant_data, context)
        
        self._add_to_history(session_id, "assistant", response)
        
        return response
    
    def _analyze_intent(self, message: str) -> Dict:
        """Analyze user intent and extract key information"""
        message_lower = message.lower()
        
        intents = {
            'property_search': any(word in message_lower for word in ['find', 'search', 'show', 'recommend']),
            'roi_analysis': any(word in message_lower for word in ['roi', 'return', 'profit', 'yield']),
            'market_trends': any(word in message_lower for word in ['trend', 'market', 'forecast', 'future']),
            'area_comparison': any(word in message_lower for word in ['compare', 'vs', 'versus', 'better']),
            'investment_advice': any(word in message_lower for word in ['advice', 'should', 'recommend', 'suggest']),
            'specific_property': any(word in message_lower for word in ['property', 'apartment', 'villa', 'penthouse'])
        }
        
        return {
            'primary_intent': max(intents, key=intents.get) if any(intents.values()) else 'general_inquiry'
        }
    
    def _retrieve_relevant_information(self, query: str, context: ChatContext) -> Dict:
        """Retrieve relevant property and market data using RAG principles"""
        relevant_properties = []
        
        query_lower = query.lower()
        user_budget = context.preferences.get('budget_range', [0, 10000000])
        
        # Filter properties based on query and user preferences
        for prop in self.property_data:
            relevance_score = 0
            
            # Budget matching
            if user_budget[0] <= prop.get('price', 0) <= user_budget[1]:
                relevance_score += 3
                
            # Opportunity score (high-quality properties)
            if prop.get('opportunity_score', 0) >= 70:
                relevance_score += 1
                
            if relevance_score >= 2:
                relevant_properties.append(prop)
        
        # Sort by relevance and take top 5
        relevant_properties.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
        
        return {
            'properties': relevant_properties[:5]
        }
    
    def _generate_response(self, user_message: str, intent: Dict, relevant_data: Dict, context: ChatContext) -> str:
        """Generate AI response using OpenAI with RAG context"""
        
        # Prepare context for AI
        properties_context = ""
        if relevant_data['properties']:
            properties_context = "\n\nRelevant Properties:\n"
            for i, prop in enumerate(relevant_data['properties'][:3], 1):
                properties_context += f"{i}. {prop.get('title', 'Property')} - AED {prop.get('price', 0):,} "
                properties_context += f"(Score: {prop.get('opportunity_score', 0)}/100, "
                properties_context += f"ROI: {prop.get('roi_potential', 'N/A')})\n"
        
        system_prompt = f"""You are an expert AI Real Estate Investment Consultant specializing in UAE and Saudi Arabia markets.

Client Budget: AED {context.preferences.get('budget_range', [800000, 2000000])}

Your personality:
- Professional yet approachable
- Data-driven and analytical
- Focused on ROI and investment value

Guidelines:
1. Always base advice on the provided property data
2. Include specific property examples when relevant
3. Provide actionable investment advice

Available Data:
{properties_context}

Respond to the user's question with specific, actionable advice."""

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ I apologize, but I'm experiencing technical difficulties. Please try again. Error: {str(e)}"
    
    def _add_to_history(self, session_id: str, role: str, content: str):
        """Add message to conversation history"""
        if session_id in self.conversation_contexts:
            self.conversation_contexts[session_id].conversation_history.append({
                'role': role,
                'content': content,
                'timestamp': datetime.now().isoformat()
            })

def main():
    """Test the chatbot system"""
    # Initialize chatbot (you'll need to set your OpenAI API key)
    chatbot = RealEstateRAGChatbot(openai_api_key=os.getenv('OPENAI_API_KEY', 'your-key-here'))
    
    # Start a test conversation
    client_prefs = {
        'budget_range': [1000000, 2500000],
        'preferred_areas': ['Palm Jumeirah', 'Downtown Dubai'],
        'experience_level': 'Intermediate'
    }
    
    session_info = chatbot.start_conversation('test_client_001', client_prefs)
    print("🤖 CHATBOT SYSTEM INITIALIZED")
    print("=" * 60)
    print(session_info)

if __name__ == "__main__":
    main()
