#!/usr/bin/env python3
"""
AI-Powered Real Estate Investment Analysis Engine
Transforms property data into actionable investment intelligence
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import statistics
from dataclasses import dataclass

@dataclass
class InvestmentOpportunity:
    property_id: str
    title: str
    area: str
    price: int
    size_sqft: int
    bedrooms: int
    price_per_sqft: float
    opportunity_score: float
    roi_potential: str
    investment_grade: str
    risk_level: str
    key_insights: List[str]

class AIInvestmentAnalyzer:
    """AI-Powered Investment Analysis Engine"""
    
    def __init__(self):
        self.market_benchmarks = self._initialize_market_data()
        self.analysis_timestamp = datetime.now()
        
    def _initialize_market_data(self) -> Dict:
        """Initialize Dubai market benchmarks and trends"""
        return {
            'area_premiums': {
                'Downtown Dubai': 1.25,
                'DIFC': 1.20,
                'Palm Jumeirah': 1.35,
                'Dubai Marina': 1.15,
                'JBR': 1.18,
                'Business Bay': 1.10,
                'City Walk': 1.22,
                'Dubai Hills': 1.08
            },
            'property_multipliers': {
                'Apartment': 1.0,
                'Townhouse': 1.05,
                'Villa': 1.15,
                'Penthouse': 1.30
            },
            'market_growth_rate': 0.08,  # 8% annual
            'rental_yields': {
                'Apartment': 0.065,  # 6.5%
                'Villa': 0.055,      # 5.5%
                'Townhouse': 0.060,  # 6.0%
                'Penthouse': 0.070   # 7.0%
            }
        }
    
    def load_property_data(self, data_file: str) -> List[Dict]:
        """Load property data from JSON file"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                properties = json.load(f)
            print(f"✅ Loaded {len(properties)} properties from {data_file}")
            return properties
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return []
    
    def calculate_market_value(self, property_data: Dict) -> float:
        """Calculate expected market value using AI benchmarks"""
        area = property_data['location_area']
        prop_type = property_data['property_type']
        size_sqft = property_data['size_sqft']
        
        # Base price per sqft for Dubai market
        base_price_per_sqft = 950  # AED
        
        # Apply area premium
        area_multiplier = self.market_benchmarks['area_premiums'].get(area, 1.0)
        
        # Apply property type premium
        type_multiplier = self.market_benchmarks['property_multipliers'].get(prop_type, 1.0)
        
        # Calculate expected market value
        expected_price_per_sqft = base_price_per_sqft * area_multiplier * type_multiplier
        expected_market_value = expected_price_per_sqft * size_sqft
        
        return expected_market_value
    
    def calculate_roi_potential(self, property_data: Dict, market_value: float) -> Tuple[float, str]:
        """Calculate ROI potential and investment grade"""
        current_price = property_data['price']
        prop_type = property_data['property_type']
        
        # Price advantage calculation
        price_advantage = (market_value - current_price) / current_price
        
        # Rental yield calculation
        rental_yield = self.market_benchmarks['rental_yields'].get(prop_type, 0.06)
        annual_rental = current_price * rental_yield
        
        # Capital appreciation (8% annual growth)
        growth_rate = self.market_benchmarks['market_growth_rate']
        
        # 5-year ROI projection
        total_roi = (price_advantage + (rental_yield * 5) + (growth_rate * 5)) * 100
        
        # Determine investment grade
        if total_roi >= 80:
            grade = "A+ EXCEPTIONAL"
        elif total_roi >= 60:
            grade = "A EXCELLENT"
        elif total_roi >= 40:
            grade = "B+ GOOD"
        elif total_roi >= 25:
            grade = "B FAIR"
        else:
            grade = "C RISKY"
            
        return total_roi, grade
    
    def calculate_opportunity_score(self, property_data: Dict, market_value: float, roi: float) -> float:
        """Calculate AI opportunity score (0-100)"""
        current_price = property_data['price']
        
        # Price efficiency (40% weight)
        price_efficiency = min(((market_value - current_price) / current_price) * 100, 40)
        price_efficiency = max(price_efficiency, 0)
        
        # ROI potential (35% weight)
        roi_score = min(roi * 0.35, 35)
        
        # Location premium (15% weight)
        area = property_data['location_area']
        location_score = (self.market_benchmarks['area_premiums'].get(area, 1.0) - 1) * 100
        location_score = min(location_score * 0.6, 15)
        
        # Property type premium (10% weight)
        prop_type = property_data['property_type']
        type_score = (self.market_benchmarks['property_multipliers'].get(prop_type, 1.0) - 1) * 100
        type_score = min(type_score, 10)
        
        total_score = price_efficiency + roi_score + location_score + type_score
        return min(total_score, 100)
    
    def assess_risk_level(self, property_data: Dict, opportunity_score: float) -> str:
        """Assess investment risk level"""
        price = property_data['price']
        area = property_data['location_area']
        
        # High-value properties have different risk profiles
        if price > 5000000:  # Above 5M AED
            if opportunity_score > 70:
                return "MODERATE-HIGH (Premium Segment)"
            else:
                return "HIGH (Luxury Risk)"
        elif price > 2000000:  # 2-5M AED
            if opportunity_score > 60:
                return "LOW-MODERATE (Stable)"
            else:
                return "MODERATE (Mid-Market)"
        else:  # Under 2M AED
            if opportunity_score > 70:
                return "LOW (High Opportunity)"
            else:
                return "MODERATE (Entry Level)"
    
    def generate_insights(self, property_data: Dict, market_value: float, roi: float, score: float) -> List[str]:
        """Generate AI-powered investment insights"""
        insights = []
        current_price = property_data['price']
        area = property_data['location_area']
        prop_type = property_data['property_type']
        price_per_sqft = property_data['price_per_sqft']
        
        # Price analysis
        price_diff = market_value - current_price
        if price_diff > 200000:
            insights.append(f"💰 UNDERVALUED: {price_diff:,.0f} AED below market value")
        elif price_diff > 50000:
            insights.append(f"💵 FAIR PRICE: {price_diff:,.0f} AED below market")
        else:
            insights.append("📊 MARKET PRICE: Aligned with current valuations")
        
        # Location insights
        if area in ['Downtown Dubai', 'DIFC', 'Palm Jumeirah']:
            insights.append(f"🌟 PRIME LOCATION: {area} offers premium appreciation")
        elif area in ['Dubai Marina', 'JBR', 'City Walk']:
            insights.append(f"🏢 STRONG LOCATION: {area} shows solid growth potential")
        
        # Property type insights
        if prop_type == 'Penthouse':
            insights.append("🏆 LUXURY SEGMENT: High rental yields & appreciation")
        elif prop_type == 'Villa':
            insights.append("🏡 FAMILY APPEAL: Strong rental demand & resale value")
        
        # ROI insights
        if roi > 70:
            insights.append(f"🚀 EXCEPTIONAL ROI: {roi:.1f}% projected 5-year returns")
        elif roi > 50:
            insights.append(f"📈 STRONG ROI: {roi:.1f}% projected returns")
        
        # Size efficiency
        avg_price_per_sqft = 1000  # Market average
        if price_per_sqft < avg_price_per_sqft * 0.9:
            insights.append(f"📏 SIZE EFFICIENCY: {price_per_sqft:.0f} AED/sqft vs {avg_price_per_sqft} market avg")
        
        return insights[:4]  # Top 4 insights
    
    def analyze_single_property(self, property_data: Dict) -> InvestmentOpportunity:
        """Analyze single property investment potential"""
        # Calculate market metrics
        market_value = self.calculate_market_value(property_data)
        roi, grade = self.calculate_roi_potential(property_data, market_value)
        score = self.calculate_opportunity_score(property_data, market_value, roi)
        risk = self.assess_risk_level(property_data, score)
        insights = self.generate_insights(property_data, market_value, roi, score)
        
        return InvestmentOpportunity(
            property_id=property_data['property_id'],
            title=property_data['title'],
            area=property_data['location_area'],
            price=property_data['price'],
            size_sqft=property_data['size_sqft'],
            bedrooms=property_data['bedrooms'],
            price_per_sqft=property_data['price_per_sqft'],
            opportunity_score=score,
            roi_potential=f"{roi:.1f}%",
            investment_grade=grade,
            risk_level=risk,
            key_insights=insights
        )
    
    def analyze_portfolio(self, properties: List[Dict]) -> Dict:
        """Analyze entire property portfolio"""
        print("🤖 AI INVESTMENT ANALYSIS ENGINE")
        print("🎯 Processing Investment Opportunities...")
        print("=" * 60)
        
        opportunities = []
        
        for i, prop in enumerate(properties, 1):
            if i % 50 == 0:
                print(f"📊 Analyzed {i}/{len(properties)} properties...")
            
            opportunity = self.analyze_single_property(prop)
            opportunities.append(opportunity)
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x.opportunity_score, reverse=True)
        
        # Generate portfolio insights
        portfolio_stats = self._generate_portfolio_stats(opportunities)
        
        print(f"✅ Analysis Complete: {len(opportunities)} opportunities analyzed")
        
        return {
            'opportunities': opportunities,
            'portfolio_stats': portfolio_stats,
            'analysis_timestamp': self.analysis_timestamp.isoformat()
        }
    
    def _generate_portfolio_stats(self, opportunities: List[InvestmentOpportunity]) -> Dict:
        """Generate portfolio-level statistics"""
        scores = [opp.opportunity_score for opp in opportunities]
        prices = [opp.price for opp in opportunities]
        
        # Grade distribution
        grades = {}
        for opp in opportunities:
            grade = opp.investment_grade.split()[0]  # Get letter grade
            grades[grade] = grades.get(grade, 0) + 1
        
        # Area analysis
        areas = {}
        for opp in opportunities:
            areas[opp.area] = areas.get(opp.area, 0) + 1
        
        return {
            'total_opportunities': len(opportunities),
            'avg_opportunity_score': statistics.mean(scores),
            'top_10_percent_threshold': sorted(scores)[int(len(scores) * 0.9)],
            'avg_price': statistics.mean(prices),
            'median_price': statistics.median(prices),
            'grade_distribution': grades,
            'area_distribution': areas,
            'exceptional_opportunities': len([o for o in opportunities if o.opportunity_score >= 80]),
            'excellent_opportunities': len([o for o in opportunities if 60 <= o.opportunity_score < 80]),
            'good_opportunities': len([o for o in opportunities if 40 <= o.opportunity_score < 60])
        }
    
    def generate_investment_report(self, analysis_results: Dict, top_n: int = 20) -> str:
        """Generate comprehensive investment report"""
        opportunities = analysis_results['opportunities'][:top_n]
        stats = analysis_results['portfolio_stats']
        
        report = []
        report.append("=" * 80)
        report.append("🤖 AI-POWERED REAL ESTATE INVESTMENT ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"📅 Generated: {self.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"🏢 Total Properties Analyzed: {stats['total_opportunities']}")
        report.append("")
        
        # Executive Summary
        report.append("📊 EXECUTIVE SUMMARY")
        report.append("-" * 40)
        report.append(f"🏆 Exceptional Opportunities (80+ Score): {stats['exceptional_opportunities']}")
        report.append(f"⭐ Excellent Opportunities (60-79 Score): {stats['excellent_opportunities']}")
        report.append(f"✅ Good Opportunities (40-59 Score): {stats['good_opportunities']}")
        report.append(f"📈 Average Opportunity Score: {stats['avg_opportunity_score']:.1f}/100")
        report.append(f"💰 Average Property Price: AED {stats['avg_price']:,.0f}")
        report.append("")
        
        # Top Investment Opportunities
        report.append(f"🎯 TOP {top_n} INVESTMENT OPPORTUNITIES")
        report.append("=" * 80)
        
        for i, opp in enumerate(opportunities, 1):
            report.append(f"\n🏠 #{i} - {opp.title}")
            report.append(f"📍 Location: {opp.area}")
            report.append(f"💰 Price: AED {opp.price:,} ({opp.price_per_sqft:.0f}/sqft)")
            report.append(f"📏 Size: {opp.size_sqft:,} sqft | {opp.bedrooms}BR")
            report.append(f"🎯 Opportunity Score: {opp.opportunity_score:.1f}/100")
            report.append(f"📈 ROI Potential: {opp.roi_potential}")
            report.append(f"🏆 Investment Grade: {opp.investment_grade}")
            report.append(f"⚠️  Risk Level: {opp.risk_level}")
            report.append("💡 Key Insights:")
            for insight in opp.key_insights:
                report.append(f"   • {insight}")
            report.append("-" * 60)
        
        # Market Analysis
        report.append("\n🌆 MARKET ANALYSIS BY AREA")
        report.append("-" * 40)
        for area, count in sorted(stats['area_distribution'].items(), key=lambda x: x[1], reverse=True):
            report.append(f"• {area}: {count} properties")
        
        # Investment Grade Distribution
        report.append("\n🏆 INVESTMENT GRADE DISTRIBUTION")
        report.append("-" * 40)
        for grade, count in sorted(stats['grade_distribution'].items()):
            report.append(f"• Grade {grade}: {count} properties")
        
        report.append("\n" + "=" * 80)
        report.append("🚀 READY FOR CLIENT PRESENTATION")
        report.append("💼 Professional Investment Intelligence Report Generated")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_analysis_results(self, analysis_results: Dict, report: str) -> Tuple[str, str]:
        """Save analysis results and report"""
        timestamp = self.analysis_timestamp.strftime("%Y%m%d_%H%M%S")
        
        # Save JSON data
        json_filename = f"../reports/investment_analysis_{timestamp}.json"
        try:
            os.makedirs("../reports", exist_ok=True)
            with open(json_filename, 'w', encoding='utf-8') as f:
                # Convert opportunities to dict for JSON serialization
                serializable_results = {
                    'opportunities': [
                        {
                            'property_id': opp.property_id,
                            'title': opp.title,
                            'area': opp.area,
                            'price': opp.price,
                            'size_sqft': opp.size_sqft,
                            'bedrooms': opp.bedrooms,
                            'price_per_sqft': opp.price_per_sqft,
                            'opportunity_score': opp.opportunity_score,
                            'roi_potential': opp.roi_potential,
                            'investment_grade': opp.investment_grade,
                            'risk_level': opp.risk_level,
                            'key_insights': opp.key_insights
                        }
                        for opp in analysis_results['opportunities']
                    ],
                    'portfolio_stats': analysis_results['portfolio_stats'],
                    'analysis_timestamp': analysis_results['analysis_timestamp']
                }
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            print(f"💾 Analysis data saved: {json_filename}")
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            json_filename = ""
        
        # Save report
        report_filename = f"../reports/investment_report_{timestamp}.txt"
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 Investment report saved: {report_filename}")
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            report_filename = ""
        
        return json_filename, report_filename

def main():
    """Main execution function"""
    print("🤖 INITIALIZING AI INVESTMENT ANALYZER...")
    
    # Initialize analyzer
    analyzer = AIInvestmentAnalyzer()
    
    # Find latest property data file
    data_dir = "../data"
    if not os.path.exists(data_dir):
        print(f"❌ Data directory not found: {data_dir}")
        return
    
    # Get most recent data file
    data_files = [f for f in os.listdir(data_dir) if f.startswith("bayut_properties_") and f.endswith(".json")]
    if not data_files:
        print("❌ No property data files found")
        return
    
    latest_file = sorted(data_files, reverse=True)[0]
    data_file_path = os.path.join(data_dir, latest_file)
    
    print(f"📂 Using data file: {latest_file}")
    
    # Load and analyze properties
    properties = analyzer.load_property_data(data_file_path)
    if not properties:
        return
    
    # Run AI analysis
    analysis_results = analyzer.analyze_portfolio(properties)
    
    # Generate investment report
    report = analyzer.generate_investment_report(analysis_results, top_n=25)
    
    # Save results
    json_file, report_file = analyzer.save_analysis_results(analysis_results, report)
    
    # Display summary
    print("\n" + "=" * 80)
    print("🎯 AI ANALYSIS COMPLETE - BUSINESS READY!")
    print("=" * 80)
    
    stats = analysis_results['portfolio_stats']
    print(f"🏆 Exceptional Opportunities: {stats['exceptional_opportunities']}")
    print(f"⭐ Excellent Opportunities: {stats['excellent_opportunities']}")
    print(f"✅ Good Opportunities: {stats['good_opportunities']}")
    print(f"📊 Average Score: {stats['avg_opportunity_score']:.1f}/100")
    
    if json_file and report_file:
        print(f"\n💾 Files Generated:")
        print(f"   📊 Analysis Data: {json_file}")
        print(f"   📄 Client Report: {report_file}")
    
    print("\n🚀 READY FOR CLIENT ACQUISITION!")
    print("💼 Professional Investment Intelligence System Complete")
    
    return analysis_results

if __name__ == "__main__":
    results = main() 