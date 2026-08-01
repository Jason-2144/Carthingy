from backend.deal_engine.config import deal_settings

class DealerProfitCalculator:
    def calculate(self, purchase_price: float, estimated_retail_value: float) -> dict:
        if purchase_price <= 0:
            return {}
            
        recon_cost = deal_settings.RECONDITIONING_COST_BASE
        trans_cost = deal_settings.TRANSPORT_COST_BASE
        reg_cost = deal_settings.REGISTRATION_COST_BASE
        
        total_investment = purchase_price + recon_cost + trans_cost + reg_cost
        
        expected_gross_profit = estimated_retail_value - total_investment
        roi = expected_gross_profit / total_investment if total_investment > 0 else 0
        profit_margin = expected_gross_profit / estimated_retail_value if estimated_retail_value > 0 else 0
        
        # Target break-even (if we want exactly target margin)
        # target_margin = (retail - target_investment) / retail
        # target_investment = retail * (1 - target_margin)
        # target_purchase = target_investment - costs
        target_investment = estimated_retail_value * (1 - deal_settings.DEALER_TARGET_MARGIN)
        break_even_purchase_price = target_investment - (recon_cost + trans_cost + reg_cost)
        
        return {
            "purchase_price": round(purchase_price, 2),
            "reconditioning_cost": round(recon_cost, 2),
            "transport_cost": round(trans_cost, 2),
            "registration_cost": round(reg_cost, 2),
            "expected_selling_price": round(estimated_retail_value, 2),
            "expected_gross_profit": round(expected_gross_profit, 2),
            "expected_roi_pct": round(roi * 100, 2),
            "profit_margin_pct": round(profit_margin * 100, 2),
            "break_even_purchase_price": round(break_even_purchase_price, 2)
        }

dealer_profit_calculator = DealerProfitCalculator()
