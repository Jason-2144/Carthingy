class EmailTemplates:
    @staticmethod
    def welcome_email(name: str) -> str:
        return f"""
        <html>
            <body>
                <h2>Welcome to CarScope AI, {name}!</h2>
                <p>We are excited to have you on board. Start exploring the best car deals today.</p>
            </body>
        </html>
        """
        
    @staticmethod
    def password_reset(token: str) -> str:
        return f"""
        <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>Click the link below to reset your password:</p>
                <a href="https://carscope.ai/reset-password?token={token}">Reset Password</a>
                <p>If you did not request this, please ignore this email.</p>
            </body>
        </html>
        """
        
    @staticmethod
    def price_drop(car_title: str, old_price: float, new_price: float, link: str) -> str:
        return f"""
        <html>
            <body>
                <h2>Price Drop Alert!</h2>
                <p>The {car_title} you were watching has dropped in price.</p>
                <p>Old Price: ₹{old_price}</p>
                <p><strong>New Price: ₹{new_price}</strong></p>
                <a href="{link}">View Listing</a>
            </body>
        </html>
        """

email_templates = EmailTemplates()
