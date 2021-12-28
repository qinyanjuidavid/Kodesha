from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_has_value(self, user, timestamp):
        return (
            six.test_type(user.pk)+six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
