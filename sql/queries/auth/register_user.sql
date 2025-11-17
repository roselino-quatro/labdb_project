SELECT *
FROM auth_register_user(
    %(cpf)s,
    %(email)s,
    %(password)s
);
