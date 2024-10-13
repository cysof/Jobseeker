from django.db import models
from jobseek .models import CustomUser
from decimal import Decimal
import uuid

TRANSCATION_TYPES = (
    ('deposit', 'Deposit'),
    ('withdrawal', 'Withdrawal'),
    ('transfer', 'Transfer'),
)


class Wallet(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default="NGN")
    phone_number = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.phone_number}: {self.balance:.2f} {self.currency}"

class UserWallet(models.Model):
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.wallet)

class CompanyWallet(models.Model):
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)
    company = models.ForeignKey('jobseek.Company', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.wallet)


class WalletAddress(models.Model):
    wallet = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.address:
            self.address = self.generate_wallet_address()
        super().save(*args, **kwargs)

    def generate_wallet_address(self):
        """
        Generates a unique wallet address based on the phone number and a random UUID.


        :return: The generated wallet address.
        :rtype: str
        """
        # Generate a random UUID
        uuid_part = uuid.uuid4().hex[:2]

        # Create a unique wallet address
        wallet_address = f"{self.wallet.phone_number}-{uuid_part}"

        return wallet_address

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSCATION_TYPES,
        default=TRANSCATION_TYPES[0][0],
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, null=True, blank=True)
    sender_address = models.ForeignKey(
        'WalletAddress',
        on_delete=models.CASCADE,
        related_name='sent_transactions',
        blank=True,
        null=True,
    )  # Optional for withdrawals
    recipient_address = models.ForeignKey(
        'WalletAddress',
        on_delete=models.CASCADE,
        related_name='received_transactions',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Return a string representation of the transaction.

        The format will vary depending on the transaction type:
            - Transfer: "sender_address -> recipient_address: amount"
            - Withdrawal: "withdrawn from user_wallet_address: amount"
        """
        if self.transaction_type == 'TRANSFER':
            return (
                f"{self.sender_address.address} -> {self.recipient_address.address}: {self.amount}"
            )
        elif self.transaction_type == 'WITHDRAWAL':
            return (
                f"withdrawn from {self.user.wallet.wallet_address.address}: {self.amount}"
            )
        else:
            return f"deposited to {self.user.wallet.wallet_address.address}: {self.amount}"

    @classmethod
    def create_transfer(
        cls,
        sender: CustomUser,
        recipient: CustomUser,
        amount: Decimal,
        description: str = "",
    ) -> 'Transaction':
        """
        Initiates a transfer between two wallets.

        Args:
            sender (CustomUser): The sender of the transfer.
            recipient (CustomUser): The recipient of the transfer.
            amount (Decimal): The amount to be transferred.
            description (str, optional): A description for the transfer.

        Returns:
            Transaction: The created transaction object.
        """
        sender_wallet = sender.wallet
        if sender_wallet.balance < amount:
            raise InsufficientBalanceError("Insufficient balance")

        transaction = cls.objects.create(
            user=sender,
            transaction_type=cls.TRANSFER,
            amount=amount,
            description=description,
            sender_address=sender_wallet.wallet_address,
            recipient_address=recipient.wallet.wallet_address,
        )

        sender_wallet.balance -= amount
        sender_wallet.save()

        recipient_wallet = recipient.wallet
        recipient_wallet.balance += amount
        recipient_wallet.save()

        return transaction

    @classmethod
    def create_withdrawal(
        cls,
        user: CustomUser,
        amount: Decimal,
        description: str = "",
    ) -> 'Transaction':
        """
        Initiates a withdrawal from a user's wallet.

        Args:
            user (CustomUser): The user withdrawing funds.
            amount (Decimal): The amount to withdraw.
            description (str, optional): A description for the withdrawal.

        Returns:
            Transaction: The created transaction object.
        """
        user_wallet = user.wallet
        if user_wallet.balance < amount:
            raise InsufficientBalanceError("Insufficient balance")

        transaction = cls.objects.create(
            user=user,
            transaction_type=cls.WITHDRAWAL,
            amount=amount,
            description=description,
            sender_address=user_wallet.wallet_address,  # Use sender's wallet address
            recipient_address=None,  # No recipient for withdrawals
        )

        user_wallet.balance -= amount
        user_wallet.save()

        return transaction
    
    @classmethod
    def create_deposit(
        cls,
        user: CustomUser,
        amount: Decimal,
        description: str = "",
    ) -> 'Transaction':
        """
        Initiates a deposit to a user's wallet.

        Args:
            user (CustomUser): The user depositing funds.
            amount (Decimal): The amount to deposit.
            description (str, optional): A description for the deposit.

        Returns:
            Transaction: The created transaction object.
        """
        transaction = cls.objects.create(
            user=user,
            transaction_type=cls.DEPOSIT,
            amount=amount,
            description=description,
            sender_address=None,  # No sender for deposits
            recipient_address=user.wallet.wallet_address,  # Use recipient's wallet address
        )

        user.wallet.balance += amount
        user.wallet.save()

        return transaction


class InsufficientBalanceError(Exception):
    """Custom exception for insufficient balance."""
    pass
