import pytest

def test_create_bear(bear_client):
    ursus = {'bear_type':'BROWN','bear_name':'VASYA','bear_age':13.0}
    data = bear_client.vr(bear_client.create_bear(ursus))
    bear_id = data.json()
    data = bear_client.vr(bear_client.show_bear(str(bear_id)))
    ursus.update({'bear_id': bear_id})
    assert ursus == data.json()

def test_delete_bear(bear_client):
    ursus = {'bear_type':'POLAR','bear_name': 'OLEG','bear_age': 7.0}
    data = bear_client.vr(bear_client.create_bear(ursus))
    bear_id = data.json()
    data = bear_client.vr(bear_client.delete_bear(str(bear_id)))
    assert data.text == 'OK'
    data = bear_client.vr(bear_client.show_bear(str(bear_id)))
    assert data.text == 'EMPTY'

def test_update_bear(bear_client):
    ursus = {'bear_type': 'BROWN', 'bear_name': 'URY', 'bear_age': 11.0}
    data = bear_client.vr(bear_client.create_bear(ursus))
    bear_id = data.json()
    ursus.update({'bear_id': bear_id})
    new_ursus = {'bear_type': 'POLAR', 'bear_name': 'IGNAT', 'bear_age': 33.0}
    data = bear_client.vr(bear_client.update_bear(str(bear_id), new_ursus))
    assert data.text == 'OK'
    #Проверяем, что мишка, которого мы изменяли по айди, действительно изменён. Так же проверяем по айди.
    data = bear_client.vr(bear_client.show_bear(str(bear_id)))
    #Добавляем в дату "нового" медведя айдишник, которого там не было
    new_ursus.update({'bear_id': bear_id})
    assert new_ursus == data.json()

def test_show_bears(bear_client):
    ursus1 = {'bear_type': 'POLAR', 'bear_name': 'FEDOR', 'bear_age': 1.0}
    ursus2 = {'bear_type': 'BLACK', 'bear_name': 'ALEX', 'bear_age': 2.0}
    ursus3 = {'bear_type': 'BROWN', 'bear_name': 'PAUL', 'bear_age': 3.0}
    #ursus4 = {'bear_type': 'GUMMY', 'bear_name': 'GLEB', 'bear_age': 4.0}
    ursus = [ursus1,ursus2,ursus3]
    for i in ursus:
        data = bear_client.vr(bear_client.create_bear(i))
        bear_id = data.json()
        i.update({'bear_id': bear_id})
    data = bear_client.vr(bear_client.show_bears())
    for i in ursus:
        assert i in data.json()

def test_delete_bears(bear_client):
    ursus1 = {'bear_type': 'POLAR', 'bear_name': 'FEDOR', 'bear_age': 1.0}
    ursus2 = {'bear_type': 'BLACK', 'bear_name': 'ALEX', 'bear_age': 2.0}
    ursus3 = {'bear_type': 'BROWN', 'bear_name': 'PAUL', 'bear_age': 3.0}
    # ursus4 = {'bear_type': 'GUMMY', 'bear_name': 'GLEB', 'bear_age': 4.0}
    # Bug
    ursus = [ursus1, ursus2, ursus3]
    for i in ursus:
        data = bear_client.vr(bear_client.create_bear(i))
    data = bear_client.vr(bear_client.delete_bears())
    assert data.text == 'OK'
    data = bear_client.vr(bear_client.show_bears())
    assert data.json() == []

@pytest.mark.negative
def test_create_bear_negative(bear_client):
    #Пробуем создать медведя с невалидными данными
    ursus = {'bear_type': 'PANDA', 'bear_name': 'PO', 'bear_age': 50.0}
    data = bear_client.create_bear(ursus)
    assert data.status_code == 500

