SELECT *
FROM auth_login(
    %(login_identifier)s,
    %(password)s,
    %(client_identifier)s
);
