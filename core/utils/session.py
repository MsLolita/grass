

class BaseClient:
    devices_id = "5b225835542d4e64754a504e326354316a222c20225577437230505a644d53624b724453222c2022453047744e6d77316a74654f677941222c20224c2d4c516255533748727367763847222c20224643396b75376d6c4e634f542d5258222c2022644d754c75514d546475656e4d6239222c20225849564149575a6855755f6d6a6750222c2022567563776547764d683479694a716e222c2022354741585651726865666c38355a58222c2022427a6c4f7455665478704346717930222c202262784a3237334b6c6d344b735f3031222c20227044614b476b394f6970517a347835222c20227a67516c4a3530695166467536664e222c202272464432666b68376a594533634278222c20223350424a4f43716962447233526d37222c20225f7a7650492d4b553565695738774a222c20225a556d6f546e566a62314e6b35796d222c202241475565446c4c576e375256695636222c2022566246794b79336d75546e37475264222c2022714c586a4464647563497a475f4554222c20225748796c3352657635316f2d674f67222c20227a414a735967504f4456667630394a222c20224b4c694b68396753545a6547617956222c20224e7370466975664c33557a33693561222c2022527565527875707938536373554a4e222c20224f584551594d506667556e43547a4b222c202233396430734851516d534d6e6c785f222c20226968726a4a4947374e386b44313233222c20224b35594961536f5677597542487238222c20227731376230666f725f654a352d476d222c20226b774e3935306e42565a4665504246222c202236304e443142317a516b796e72576b222c20223858716e6877775066647053305a59222c202245385635784f56436e325943704354222c20224958465139506374574c575a374270222c202236314e386c4435416c704e6843796e222c20226f6b7447306c4f4f71655666705179222c20227079766d7a6e6d3476323849664737222c20226c36695f6f7a675f67663357514332222c202238485832527557625a447575767343222c202263474530436f76516b58642d2d6141222c2022766a433762574e6c424f3930563063222c202248615543514d6b5951493466665f4d222c20227350454f3633374a39635f4e537351222c20224b5979384255754e574b2d41437851222c2022783030324951376e476b7252417a54222c2022613378784655446b73463941796638222c202271533174565778744c563231414243222c202268496345582d5a6278733939724264222c2022544f694c34772d4e6f4b5975485348222c2022314d613559466b514641566431524e222c2022766153336a30775a6f52685a49306e222c20225f7a6e593235347233315067503136222c202230763563566276686c744461784d67222c20225272526347764d3648654a30754252222c20224b353249586c436a52737658736376222c202252596774496c625f46774d75683259222c2022646364353979485736537a50386345222c20223830414f465a5968344a5a56616761222c20227235737358526c645764633949524b222c20226573675231617a5f6f47535572534d222c2022796c7439657a4e31594f70494d5735222c2022307545745a33476d4c645655376171222c20226930396c344a704a336476334a364b222c2022323267616b56727a5a315145495945222c20222d30472d6c465462316335764e5635222c2022427230686372314e7258336f697465222c20226e56364170496e326d674259464d6c222c20227a4638764743597777706853417663222c2022457a3249425171544b497a70797148222c20226b7773437038534e78674c30624362222c2022394a51704c5949526e71474f6f3369222c2022524f68664364767a327152786d3136222c202243527355784c5646786b30394f5a36222c20226d384f6d50724644674f4134474450222c2022334159762d664461466a6246787537222c20224f5868507a4772397a6130366a3042222c2022444f4a38356b5a6256673054587174222c2022796e435a52633951567368424a486c222c202251616365694c527642384565776e4f222c202246314e65357464384444786c6d7639222c20226f7253565349354542574638503156222c2022515a4b6f3867566a79645555544766222c20224363505962763565583964646e5477222c202257345557612d6e4c35423856593573222c202254454574416b6f4430685641657836222c20224e73594953795a5870356f466e6677222c20226c4930484a464d4f2d6f62776f5377222c2022426656493056563572307947536459222c20226669426e6935764d72636d6e335473222c2022344e706359706e6c654b7154314662222c2022635777436d43576762564f4a4d4f59222c202273616b6e544e564e3751672d6f4952222c20224f6558323772684e34436447797170222c202231686d68313657614e526b364b4a34222c20224a66674352566b4171722d576e6844222c20226c6e794f76744f6146303171745854222c202273353874425049646a564543327558222c20225674426946307958526b394c515359225d"

    def __init__(self, user_agent: str, proxy: str = None):
        self.session = None
        self.ip = None
        self.username = None
        self.proxy = None

        self.devices_id = BaseClient.devices_id
        self.user_agent = user_agent
        self.proxy = proxy

        self.website_headers = {
            'authority': 'api.getgrass.io',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://app.getgrass.io/register/?referralCode=qG_Fl7T6ueZuF1v',
            'referer': 'https://app.getgrass.io/register/?referralCode=qG_Fl7T6ueZuF1v',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent,
        }
