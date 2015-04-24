#####
import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db() 

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'] )

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def change_password(self, username, password, confirm_password):
        return self.app.post('/change_password', data=dict(
            username=username,
            password=password,
            comfirm_password=confirm_password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
 
    def test_change_password(self):
        self.connect_db().execute('insert into userPassword values(?,?)',['admin','default'])
        self.connect_db().execute('insert into userPassword values(?,?)',['jim','bean'])
        self.app.post('/login', data=dict(
            username='admin',
            password='default'
        ), follow_redirects=True)
        rv = self.change_password('jim','1234','1234')
        print rv.data
        assert 'Successfully changed user password' in rv.data
        rv = self.logout()


    def test_multiple_login_logout(self):

        # Test jim login with old password
        rv = self.login('jim', 'bean')
        assert 'Invalid password' in rv.data

        # Test jim login with new password
        rv = self.login('jim', '1234')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data

if __name__ == '__main__':
    unittest.main()