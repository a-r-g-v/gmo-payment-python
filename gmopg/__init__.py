# coding: utf-8
import requests
import urlparse
from errors import Error

API_BASE_URL_PRODUCTION = 'https://p01.mul-pay.jp/payment/'
API_BASE_URL_DEVELOPMENT = 'https://pt01.mul-pay.jp/payment/'

DEFAULT_TIMEOUT = 30


class ResponseError(Exception):

    def __init__(self, response):
        self.error = self.parse(response.data)

    def __str__(self):
        return "Response contains Error: " + repr(self.error)

    def __repr__(self):
        return self.__str__()

    def parse(self, response):
        dict_list = [Error(i).to_dict() for i in response['ErrInfo'].split('|')]
        return {k: v for dic in dict_list for k, v in dic.items()}


class Response(object):

    def __init__(self, response_text):
        self.data = self.decode(response_text)
        self.ok = bool('ErrCode' not in self.data)

    def decode(self, response_text):
        response_dict = urlparse.parse_qs(response_text)
        # parse_qs は {"key": ["value"]} という dict を返却するので，扱いやすいように {"key": "value"} に変換する
        return {k: v[0] for k, v in response_dict.items()}

    def parse(self, ignores=[]):
        """
            self.data = {'CardName': 'poe|foo', 'CardNo': '1111|2222'} を， [{'CardName': 'poe', 'CardNo': '1111'}. {'CardName': 'foo', 'CardNo': '2222'}] のように直して返却します
            ignoresでは，self.dataに存在するキーの名前をリストで指定でき，そのキーを返却結果に含めないようにすることができます。
        """
        assert type(self.data) is dict
        assert type(ignores) is list

        result = {}
        for k, v in self.data.items():
            if k in ignores:
                continue

            for i2, v2 in enumerate(str(v).split('|')):
                if i2 not in result:
                    result[i2] = {}
                result[i2][k] = v2

        return result.values()


class BaseAPI(object):

    def __init__(self, timeout=DEFAULT_TIMEOUT, production=False):
        self.timeout = timeout
        self.api_base_url = API_BASE_URL_PRODUCTION if production else API_BASE_URL_DEVELOPMENT

    def _requests(self, method, path, **kwargs):

        response = method(self.api_base_url + path, timeout=self.timeout, **kwargs)

        response.raise_for_status()

        print response.text
        # assert False

        response = Response(response.text)

        if not response.ok:
            raise ResponseError(response)

        return response

    def get(self, path, **kwargs):
        return self._requests(requests.get, path, **kwargs)

    def post(self, path, **kwargs):
        return self._requests(requests.post, path, **kwargs)

    def assertRequiredOptions(self, key, options):
        for i in key:
            assert i in options


class Member(BaseAPI):

    def save(self, options={}):
        """
            指定されたサイトに会員を登録します。

            SiteID  char(13)
            SitePass    char(20)
            MemberID    char(60)
            MemberName  char(255) 登録する名前
        """
        self.assertRequiredOptions(["SiteID", "SitePass", "MemberID"], options)
        return self.post("SaveMember.idPass", data=options)

    def update(self, options={}):
        """
            指定されたサイトに会員情報を更新します。
            SiteID  char(13)
            SitePass    char(20)
            MemberID    char(60)
            MemberName  char(255) 更新する名前
        """
        self.assertRequiredOptions(["SiteID", "SitePass", "MemberID"], options)
        return self.post("UpdateMember.idPass", data=options)

    def delete(self, options={}):
        """
            指定したサイトから会員情報を削除します。
            SiteID  char(13)
            SitePass    char(20)
            MemberID    char(60)
        """

        self.assertRequiredOptions(["SiteID", "SitePass", "MemberID"], options)
        return self.post("DeleteMember.idPass", data=options)

    def search(self, options={}):
        """
            指定したサイトの会員情報を参照します。
            SiteID  char(13)
            SitePass    char(20)
            MemberID    char(60)
        """
        self.assertRequiredOptions(["SiteID", "SitePass", "MemberID"], options)
        return self.post("SearchMember.idPass", data=options)


class Card(BaseAPI):

    def save(self, options={}):
        """
            指定した会員にカード情報を登録します。尚、サイトに設定されたショップ ID を使用してカード会社と通信を行い有効性の確認を行います。

            SiteID  CHAR(13)
            SitePass    CHAR(20)
            MemberID    CHAR(60)
            SeqMode     CHAR(1)
            CardSeq     NUMBER(4)
            DefaultFlag CHAR(1) 0(継続課金対象としない, デフォルト値), 1(継続課金対象とする)
            CardName    CHAR(10)
            CardNo      CHAR(16)
            CardPass    CHAR(20)
            Expire      CHAR(4)
            HolderName  CHAR(50) 名義人
        """
        self.assertRequiredOptions(['SiteID', 'SitePass', 'MemberID', 'CardNo', 'Expire'], options)
        return self.post('SaveCard.idPass', data=options)

    def delete(self, options={}):
        """
            指定した会員のカード情報を削除します。

            SiteID
            SitePass
            MemberID
            SeqMode
            CardSeq CHAR(4) 削除を行うカードの登録連番を設定します。
        """
        self.assertRequiredOptions(['SiteID', 'SitePass', 'MemberID', 'CardSeq'], options)
        return self.post('DeleteCard.idPass', data=options)

    def search(self, options={}):
        """
            指定した会員のカード情報を参照します。

            SiteID
            SitePass
            MemberID
            SeqMode
            CardSeq
        """
        self.assertRequiredOptions(['SiteID', 'SitePass', 'MemberID', 'SeqMode'], options)
        return self.post('SearchCard.idPass', data=options)

    def traded(self, options={}):
        """
            指定されたオーダーID の取引に使用したカードを登録します。

            ShopID
            ShopPass
            OrderID
            SiteID
            SitePass
            MemberID
            SeqMode
            DefaultFlag
            HolderName
        """
        self.assertRequiredOptions(['ShopID', 'ShopPass', 'OrderID', 'SiteID', 'SitePass', 'MemberID'], options)
        return self.post('TradedCard.idPass', data=options)


class Trade(BaseAPI):

    def search(self, options={}):
        """
            指定したオーダーID の取引情報を取得します。

            ShopID
            ShopPass
            OrderID
        """
        self.assertRequiredOptions(['ShopID', 'ShopPass', 'OrderID'], options)
        return self.post('SearchTrade.idPass', data=options)


class Tran(BaseAPI):

    def entry(self, options={}):
        """
            取引登録 API
            これ以降の決済取引で必要となる取引 ID と取引パスワードの発行を行い、取引を開始します。

            ShopID  char(13)
            ShopPass    char(10)
            OrderID char(27)    取引を識別するID
            JobCd   char    処理区分 CHECK / CAPTURE / AUTH / SAUTH
            Amount  number(7)   処理区分が有効性チェック(CHECK)を除き必須，利用金額
            Tax number(7) 税送料
            TdFlag char(1)  本人認証サービスを使用するかどうか 0 or 1
            TdTenantName    char    3Dセキュア表示店舗名
        """
        # TODO 3D セキュア系は後で実装する

        self.assertRequiredOptions(['ShopID', 'ShopPass', 'OrderID', 'JobCd'], options)
        assert options["JobCd"] == "CHECK" or options["Amount"] is not None

        return self.post('EntryTran.idPass', data=options)

    def execute(self, options={}):
        """
            決済実行 API
            お客様が入力したカード番号と有効期限の情報でカード会社と通信を行い決済を実施し、結果を返します。

            AccessID    char(32)
            AccessPass  char(32)
            OrderID     char(27)
            Method      char(1)    1(一括), 2(分割), 3(ボーナス一括), 4(ボーナス分割), 5(リボ), 処理区分 JobCdがCHECKの場合以外必要
            PayTimes    number(2)   支払い回数，Methodが分割，ボーナス分割を示している場合は必須
            CardNo      char(16)
            Expire      char(4)     YYMM カード有効期限
            PIN         char(4)     決済に使用するクレジッドカードの暗証番号を設定(別途オプション契約が必要)
            ClientField1 char(100) 自由項目
            ClientField2 char(100)
            ClientField3 char(100)
            ClientFieldFlag char(1)

            GMOPGに登録しているユーザ情報，カード情報を用いて決済する場合は下記のパラメタを付与する必要がある。

            SiteID  required
            SitePass required
            MemberID required
            SeqMode
            CardSeq required
            CardPass
            SecurityCode
        """
        self.assertRequiredOptions(['AccessID', 'AccessPass', 'OrderID', 'CardNo', 'Expire'], options)
        assert ('Method' not in options or options['Method'] % 2 != 0) or 'PayTimes' in options

        return self.post('ExecTran.idPass', data=options)

    def change(self, options={}):
        """
            決済が完了した取引に対して金額の変更を行います。

            ShopID
            ShopPass
            AccessID
            AccessPass
            JobCd CAPTURE / AUTH / SAUTH
            Amount
            Tax
        """
        self.assertRequiredOptions(['ShopID', 'ShopPass', 'AccessID', 'AccessPass', 'JobCd', 'Amount'], options)
        return self.post('ChangeTran.idPass', data=options)

    def alter(self, options={}):
        """
            1. 決済が完了した取引に対して決済内容の取り消しを行います。指定された取引情報を使用してカード会社と通信を行い取り消しを実施します。
            2. 取り消されている決済に対して再オーソリを行います。指定された決済情報を使用してカード会社と通信を行い実施します
            3. 仮売上の決済に対して実売上を行います。尚、実行時に仮売上時との金額チェックを行います。

            ShopID
            ShopPass
            AccessID
            AccessPass
            JobCd CHAR : VOID(取り消し) / RETURN(返品) / RETURNX(月跨り返品) / CAPTURE(即時売上) / AUTH(仮売上) / SALES(実売上)

            JobCdがCAPTURE / AUTH の場合は以下のパラメタが使用可能です

            Amount NUMBER(7) required
            Tax NUMBER(7)
            Method      char(1)    1(一括), 2(分割), 3(ボーナス一括), 4(ボーナス分割), 5(リボ), 処理区分 JobCdがCHECKの場合以外必要
            PayTimes    number(2)   支払い回数，Methodが分割，ボーナス分割を示している場合は必須

            JobCdがSALESの場合は以下のパラメタが使用可能です
            Amount NUMBER(7)    仮売上登録時に指定した金額
        """

        self.assertRequiredOptions(['ShopID', 'ShopPass', 'AccessID', 'AccessPass', 'JobCd'], options)
        return self.post('AlterTran.idPass', data=options)


class GMOPG(object):

    def __init__(self, timeout=DEFAULT_TIMEOUT, production=True):
        self.tran = Tran(timeout=timeout, production=production)
        self.card = Card(timeout=timeout, production=production)
        self.member = Member(timeout=timeout, production=production)
        self.trade = Trade(timeout=timeout, production=production)
