import pytest
from flask import session
from flask_login import current_user
from flaskDir import app, db
from sqlalchemy_utils import create_database, database_exists
from flaskDir.MediCare.model.entity.Medici import Medico
from flaskDir.MediCare.model.entity.EnteSanitario import EnteSanitario
from flaskDir.source.EnteFunction.EnteService import EnteService


class TestEnte():
    @pytest.fixture(autouse=True, scope='session')
    def setUp(self, request):
        from urllib.parse import quote

        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{quote('Cancello1@')}@localhost:3306/testmedicare"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["TESTING"] = True
        db.init_app(app)

        with app.test_client():
            with app.app_context():

                if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
                    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

                db.create_all()

            def teardown():

                with app.app_context():
                    db.session.close_all()
                    db.drop_all()

            request.addfinalizer(teardown)


    def test_addMedico(self):
        with app.app_context():
            ente = EnteSanitario()
            ente.nome = "Ospedale Papa Giovanni XXIII"
            ente.email="ospedaleBergamo23@pec.it"
            ente.password_hash = "Papa23"
            ente.città = "Bergamo"
            db.session.add(ente)
            db.session.commit()

            result = EnteService.creaReparto("RepartoCardiologia","ospedaleBergamo23Cardiologia@pec.it","Papa23","Cardiologia","Bergamo","ospedaleBergamo23@pec.it")
            oracle = True
            assert oracle == result
            reparto=Medico.query.filter_by(email="ospedaleBergamo23Cardiologia@pec.it").first()
            assert reparto

            db.session.delete(reparto)
            db.session.delete(ente)
            db.session.commit()

    def test_addMedicoInvalid(self):
        with app.app_context():
            ente = EnteSanitario()
            ente.nome = "Ospedale Papa Giovanni XXIII"
            ente.email = "ospedaleBergamo23@pec.it"
            ente.password_hash = "Papa23"
            ente.città = "Bergamo"
            db.session.add(ente)
            db.session.commit()

            result = EnteService.creaReparto("RepartoCardiologia", "ospedaleBergamo23Cardiologia@pec.it",
                                                     "Papa23", "Cardiologia", "Bergamo", "ospedaleBergamo23")
            oracle = False
            assert oracle == result
            reparto = Medico.query.filter_by(email="ospedaleBergamo23Cardiologia@pec.it").first()
            assert not reparto

            db.session.delete(ente)
            db.session.commit()
