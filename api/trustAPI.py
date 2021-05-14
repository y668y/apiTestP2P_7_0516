import app


class trustAPI():
    def __init__(self):
        self.trust_register_url=app.BASE_URL+"/trust/trust/register"
        self.get_recharge_verify_code_url=app.BASE_URL+"/common/public/verifycode/"
        self.recharge_url=app.BASE_URL+"/trust/trust/recharge"

    def trust_register(self,session):
        return session.post(self.trust_register_url)

    def get_recharge_verify_code(self,session,r):
        url=self.get_recharge_verify_code_url+r
        return session.get(url)

    def recharge(self,session,amout="1000",code="8888"):
        data={
        "paymentType":"chinapnrTrust",
        "amount":amout,
        "formStr":"reForm",
        "valicode":code
        }
        response=session.post(self.recharge_url,data)
        return response





