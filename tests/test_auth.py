def registrar_usuario_de_prueba(cliente, correo="test@mail.com", password="test1234"):
    return cliente.post("/auth/registro", data={
        "nombre": "Usuario Test",
        "correo": correo,
        "contrasena": password,
        "rol": "paciente",
    }, follow_redirects=False)


def test_registrar_usuario_post_redirige(cliente):
    resp = registrar_usuario_de_prueba(cliente)
    assert resp.status_code in (301, 302, 303, 307, 308)


def test_login_usuario_post_retorna_200(cliente):
    registrar_usuario_de_prueba(cliente, correo="login@mail.com")
    resp = cliente.post("/auth/iniciar-sesion", data={
        "correo": "login@mail.com",
        "contrasena": "test1234",
    }, follow_redirects=True)
    assert resp.status_code == 200
