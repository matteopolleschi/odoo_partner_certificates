# odoo_partner_certificates

Module build to add certificate feature to the core module res_partner:
    - create a certificate (name, expiry date, issuer, reminder and attachments).
    - a partner can have multiple certificates.
    - a certificate contains multiple attachments.
    - when certificate is expired company receive a reminder mail.
    - When partner is created a user is created for it in quiz.
    - When partner is deleted the user is desactivated in quiz.

There is a function to sens the logins of the newly created odoo partner/quiz user to his email; 
uncomment it in order to trigger a mail to the partner. Prerequisite: it needs an active mail server configured.