def test_inicio_retorna_200(cliente):
    assert cliente.get("/").status_code == 200


def test_pagina_login_retorna_200(cliente):
    assert cliente.get("/auth/iniciar-sesion").status_code == 200


def test_pagina_registro_retorna_200(cliente):
    assert cliente.get("/auth/registro").status_code == 200


def test_lista_medicos_retorna_200(cliente):
    assert cliente.get("/medicos/").status_code == 200


def test_medico_no_existe_retorna_404(cliente):
    assert cliente.get("/medicos/9999").status_code == 404
