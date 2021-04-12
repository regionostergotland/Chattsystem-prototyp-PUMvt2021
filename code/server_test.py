import server_setup


def test_client_config():
    client1 = server_setup.add_client(
        "sid",
        "name",
        "backgroundColor",
        "userIconSource",
        server_setup.Roles["odefinierad"]
    )
    client2 = server_setup.get_client("sid")
    assert client1 == client2
    assert client2.sid == "sid"
    assert client2.name == "name"
    assert client2.backgroundColor == "backgroundColor"
    assert client2.userIconSource == "userIconSource"
    assert client2.role == server_setup.Roles["odefinierad"]
    assert server_setup.get_client("") == {}
