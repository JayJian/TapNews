import mongodb_client as client

def basic_test():
    db = client.get_db('test')
    db.demo.drop()
    assert db.demo.count() == 0
    db.demo.insert({'test':123})
    assert db.demo.count() == 1
    db.demo.drop()
    assert db.demo.count() == 0

    print 'basic_test passed!'

if __name__ == "__main__":
    basic_test()
