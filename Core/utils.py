class Utils:
    @staticmethod
    def currency_format(amount: float) -> str:
        """
        Format a currency string to a more readable format.
        """
        return f"$ {amount:,.2f}"
    
    @staticmethod
    def decimal_format(num):
        """
        rounding to nearest 2 decimal places 
        """
        return f"{num:,.2f}"
    @staticmethod
    def formater(num):
        """
        adding comma format
        """
        return f"{num:,}"