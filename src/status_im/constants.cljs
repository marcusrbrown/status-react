(ns status-im.constants
  (:require [status-im.ethereum.core :as ethereum]
            [status-im.i18n :as i18n]
            [status-im.utils.config :as config]))

(def ethereum-rpc-url "http://localhost:8545")

(def ms-in-bg-for-require-bioauth 5000)

(def content-type-text "text/plain")
(def content-type-sticker "sticker")
(def content-type-status "status")
(def content-type-command "command")
(def content-type-command-request "command-request")
(def content-type-emoji "emoji")

(def desktop-content-types
  #{content-type-text content-type-emoji content-type-status})

(def min-password-length 6)
(def max-group-chat-participants 10)
(def default-number-of-messages 20)
(def blocks-per-hour 120)
(def one-earth-day 86400)
(def two-pane-min-width 640)
(def left-pane-min-width 320)

(def mailserver-password "status-offline-inbox")

(def default-network config/default-network)

(def system "system")

(def mainnet-networks
  {"mainnet_rpc" {:id     "mainnet_rpc",
                  :name   "Mainnet with upstream RPC",
                  :config {:NetworkId      (ethereum/chain-keyword->chain-id :mainnet)
                           :DataDir        "/ethereum/mainnet_rpc"
                           :UpstreamConfig {:Enabled true
                                            :URL     "https://mainnet.infura.io/v3/f315575765b14720b32382a61a89341a"}}}})

(def sidechain-networks
  {"xdai_rpc" {:id     "xdai_rpc",
               :name   "xDai Chain",
               :config {:NetworkId      (ethereum/chain-keyword->chain-id :xdai)
                        :DataDir        "/ethereum/xdai_rpc"
                        :UpstreamConfig {:Enabled true
                                         :URL     "https://dai.poa.network"}}}
   "poa_rpc"  {:id     "poa_rpc",
               :name   "POA Network",
               :config {:NetworkId      (ethereum/chain-keyword->chain-id :poa)
                        :DataDir        "/ethereum/poa_rpc"
                        :UpstreamConfig {:Enabled true
                                         :URL     "https://core.poa.network"}}}})

(def testnet-networks
  {"testnet_rpc" {:id     "testnet_rpc",
                  :name   "Ropsten with upstream RPC",
                  :config {:NetworkId      (ethereum/chain-keyword->chain-id :testnet)
                           :DataDir        "/ethereum/testnet_rpc"
                           :UpstreamConfig {:Enabled true
                                            :URL     "https://ropsten.infura.io/v3/f315575765b14720b32382a61a89341a"}}}
   "rinkeby_rpc" {:id     "rinkeby_rpc",
                  :name   "Rinkeby with upstream RPC",
                  :config {:NetworkId      (ethereum/chain-keyword->chain-id :rinkeby)
                           :DataDir        "/ethereum/rinkeby_rpc"
                           :UpstreamConfig {:Enabled true
                                            :URL     "https://rinkeby.infura.io/v3/f315575765b14720b32382a61a89341a"}}}
   "goerli_rpc"  {:id     "goerli_rpc",
                  :name   "Goerli with upstream RPC",
                  :config {:NetworkId      (ethereum/chain-keyword->chain-id :goerli)
                           :DataDir        "/ethereum/goerli_rpc"
                           :UpstreamConfig {:Enabled true
                                            :URL     "https://goerli.blockscout.com/"}}}})

(def default-networks
  (merge testnet-networks mainnet-networks sidechain-networks))

(def default-multiaccount-settings
  {:web3-opt-in?     true
   :preview-privacy? false
   :wallet           {:visible-tokens {}}})

(def currencies
  {:aed {:id :aed :code "AED" :display-name (i18n/label :t/currency-display-name-aed) :symbol "د.إ"}
   :afn {:id :afn :code "AFN" :display-name (i18n/label :t/currency-display-name-afn) :symbol "؋"}
   :ars {:id :ars :code "ARS" :display-name (i18n/label :t/currency-display-name-ars) :symbol "$"}
   :aud {:id :aud :code "AUD" :display-name (i18n/label :t/currency-display-name-aud) :symbol "$"}
   :bbd {:id :bbd :code "BBD" :display-name (i18n/label :t/currency-display-name-bbd) :symbol "$"}
   :bdt {:id :bdt :code "BDT" :display-name (i18n/label :t/currency-display-name-bdt) :symbol " Tk"}
   :bgn {:id :bgn :code "BGN" :display-name (i18n/label :t/currency-display-name-bgn) :symbol "лв"}
   :bhd {:id :bhd :code "BHD" :display-name (i18n/label :t/currency-display-name-bhd) :symbol "BD"}
   :bnd {:id :bnd :code "BND" :display-name (i18n/label :t/currency-display-name-bnd) :symbol "$"}
   :bob {:id :bob :code "BOB" :display-name (i18n/label :t/currency-display-name-bob) :symbol "$b"}
   :brl {:id :brl :code "BRL" :display-name (i18n/label :t/currency-display-name-brl) :symbol "R$"}
   :btn {:id :btn :code "BTN" :display-name (i18n/label :t/currency-display-name-btn) :symbol "Nu."}
   :cad {:id :cad :code "CAD" :display-name (i18n/label :t/currency-display-name-cad) :symbol "$"}
   :chf {:id :chf :code "CHF" :display-name (i18n/label :t/currency-display-name-chf) :symbol "CHF"}
   :clp {:id :clp :code "CLP" :display-name (i18n/label :t/currency-display-name-clp) :symbol "$"}
   :cny {:id :cny :code "CNY" :display-name (i18n/label :t/currency-display-name-cny) :symbol "¥"}
   :cop {:id :cop :code "COP" :display-name (i18n/label :t/currency-display-name-cop) :symbol "$"}
   :crc {:id :crc :code "CRC" :display-name (i18n/label :t/currency-display-name-crc) :symbol "₡"}
   :czk {:id :czk :code "CZK" :display-name (i18n/label :t/currency-display-name-czk) :symbol "Kč"}
   :dkk {:id :dkk :code "DKK" :display-name (i18n/label :t/currency-display-name-dkk) :symbol "kr"}
   :dop {:id :dop :code "DOP" :display-name (i18n/label :t/currency-display-name-dop) :symbol "RD$"}
   :egp {:id :egp :code "EGP" :display-name (i18n/label :t/currency-display-name-egp) :symbol "£"}
   :etb {:id :etb :code "ETB" :display-name (i18n/label :t/currency-display-name-etb) :symbol "Br"}
   :eur {:id :eur :code "EUR" :display-name (i18n/label :t/currency-display-name-eur) :symbol "€"}
   :gbp {:id :gbp :code "GBP" :display-name (i18n/label :t/currency-display-name-gbp) :symbol "£"}
   :gel {:id :gel :code "GEL" :display-name (i18n/label :t/currency-display-name-gel) :symbol "₾"}
   :ghs {:id :ghs :code "GHS" :display-name (i18n/label :t/currency-display-name-ghs) :symbol "¢"}
   :hkd {:id :hkd :code "HKD" :display-name (i18n/label :t/currency-display-name-hkd) :symbol "$"}
   :hrk {:id :hrk :code "HRK" :display-name (i18n/label :t/currency-display-name-hrk) :symbol "kn"}
   :huf {:id :huf :code "HUF" :display-name (i18n/label :t/currency-display-name-huf) :symbol "Ft"}
   :idr {:id :idr :code "IDR" :display-name (i18n/label :t/currency-display-name-idr) :symbol "Rp"}
   :ils {:id :ils :code "ILS" :display-name (i18n/label :t/currency-display-name-ils) :symbol "₪"}
   :inr {:id :inr :code "INR" :display-name (i18n/label :t/currency-display-name-inr) :symbol "₹"}
   :isk {:id :isk :code "ISK" :display-name (i18n/label :t/currency-display-name-isk) :symbol "kr"}
   :jmd {:id :jmd :code "JMD" :display-name (i18n/label :t/currency-display-name-jmd) :symbol "J$"}
   :jpy {:id :jpy :code "JPY" :display-name (i18n/label :t/currency-display-name-jpy) :symbol "¥"}
   :kes {:id :kes :code "KES" :display-name (i18n/label :t/currency-display-name-kes) :symbol "KSh"}
   :krw {:id :krw :code "KRW" :display-name (i18n/label :t/currency-display-name-krw) :symbol "₩"}
   :kwd {:id :kwd :code "KWD" :display-name (i18n/label :t/currency-display-name-kwd) :symbol "د.ك"}
   :kzt {:id :kzt :code "KZT" :display-name (i18n/label :t/currency-display-name-kzt) :symbol "лв"}
   :lkr {:id :lkr :code "LKR" :display-name (i18n/label :t/currency-display-name-lkr) :symbol "₨"}
   :mad {:id :mad :code "MAD" :display-name (i18n/label :t/currency-display-name-mad) :symbol "MAD"}
   :mdl {:id :mdl :code "MDL" :display-name (i18n/label :t/currency-display-name-mdl) :symbol "MDL"}
   :mur {:id :mur :code "MUR" :display-name (i18n/label :t/currency-display-name-mur) :symbol "₨"}
   :mwk {:id :mwk :code "MWK" :display-name (i18n/label :t/currency-display-name-mwk) :symbol "MK"}
   :mxn {:id :mxn :code "MXN" :display-name (i18n/label :t/currency-display-name-mxn) :symbol "$"}
   :myr {:id :myr :code "MYR" :display-name (i18n/label :t/currency-display-name-myr) :symbol "RM"}
   :mzn {:id :mzn :code "MZN" :display-name (i18n/label :t/currency-display-name-mzn) :symbol "MT"}
   :nad {:id :nad :code "NAD" :display-name (i18n/label :t/currency-display-name-nad) :symbol "$"}
   :ngn {:id :ngn :code "NGN" :display-name (i18n/label :t/currency-display-name-ngn) :symbol "₦"}
   :nok {:id :nok :code "NOK" :display-name (i18n/label :t/currency-display-name-nok) :symbol "kr"}
   :npr {:id :npr :code "NPR" :display-name (i18n/label :t/currency-display-name-npr) :symbol "₨"}
   :nzd {:id :nzd :code "NZD" :display-name (i18n/label :t/currency-display-name-nzd) :symbol "$"}
   :omr {:id :omr :code "OMR" :display-name (i18n/label :t/currency-display-name-omr) :symbol "﷼"}
   :pen {:id :pen :code "PEN" :display-name (i18n/label :t/currency-display-name-pen) :symbol "S/."}
   :pgk {:id :pgk :code "PGK" :display-name (i18n/label :t/currency-display-name-pgk) :symbol "K"}
   :php {:id :php :code "PHP" :display-name (i18n/label :t/currency-display-name-php) :symbol "₱"}
   :pkr {:id :pkr :code "PKR" :display-name (i18n/label :t/currency-display-name-pkr) :symbol "₨"}
   :pln {:id :pln :code "PLN" :display-name (i18n/label :t/currency-display-name-pln) :symbol "zł"}
   :pyg {:id :pyg :code "PYG" :display-name (i18n/label :t/currency-display-name-pyg) :symbol "Gs"}
   :qar {:id :qar :code "QAR" :display-name (i18n/label :t/currency-display-name-qar) :symbol "﷼"}
   :ron {:id :ron :code "RON" :display-name (i18n/label :t/currency-display-name-ron) :symbol "lei"}
   :rsd {:id :rsd :code "RSD" :display-name (i18n/label :t/currency-display-name-rsd) :symbol "Дин."}
   :rub {:id :rub :code "RUB" :display-name (i18n/label :t/currency-display-name-rub) :symbol "₽"}
   :sar {:id :sar :code "SAR" :display-name (i18n/label :t/currency-display-name-sar) :symbol "﷼"}
   :sek {:id :sek :code "SEK" :display-name (i18n/label :t/currency-display-name-sek) :symbol "kr"}
   :sgd {:id :sgd :code "SGD" :display-name (i18n/label :t/currency-display-name-sgd) :symbol "$"}
   :thb {:id :thb :code "THB" :display-name (i18n/label :t/currency-display-name-thb) :symbol "฿"}
   :ttd {:id :ttd :code "TTD" :display-name (i18n/label :t/currency-display-name-ttd) :symbol "TT$"}
   :twd {:id :twd :code "TWD" :display-name (i18n/label :t/currency-display-name-twd) :symbol "NT$"}
   :tzs {:id :tzs :code "TZS" :display-name (i18n/label :t/currency-display-name-tzs) :symbol "TSh"}
   :try {:id :try :code "TRY" :display-name (i18n/label :t/currency-display-name-try) :symbol "₺"}
   :uah {:id :uah :code "UAH" :display-name (i18n/label :t/currency-display-name-uah) :symbol "₴"}
   :ugx {:id :ugx :code "UGX" :display-name (i18n/label :t/currency-display-name-ugx) :symbol "USh"}
   :uyu {:id :uyu :code "UYU" :display-name (i18n/label :t/currency-display-name-uyu) :symbol "$U"}
   :usd {:id :usd :code "USD" :display-name (i18n/label :t/currency-display-name-usd) :symbol "$"}
   :vef {:id :vef :code "VEF" :display-name (i18n/label :t/currency-display-name-vef) :symbol "Bs"}
   :vnd {:id :vnd :code "VND" :display-name (i18n/label :t/currency-display-name-vnd) :symbol "₫"}
   :zar {:id :zar :code "ZAR" :display-name (i18n/label :t/currency-display-name-zar) :symbol "R"}})

;; Used to generate topic for contact discoveries
(def contact-discovery "contact-discovery")

(def ^:const send-transaction-failed-parse-response 1)
(def ^:const send-transaction-failed-parse-params   2)
(def ^:const send-transaction-no-account-selected   3)
(def ^:const send-transaction-invalid-tx-sender     4)
(def ^:const send-transaction-err-decrypt           5)

(def ^:const web3-send-transaction "eth_sendTransaction")
(def ^:const web3-personal-sign "personal_sign")
(def ^:const web3-sign-typed-data "eth_signTypedData")
(def ^:const web3-sign-typed-data-v3 "eth_signTypedData_v3")

(def ^:const web3-get-logs "eth_getLogs")
(def ^:const web3-transaction-receipt "eth_getTransactionReceipt")
(def ^:const web3-new-filter "eth_newFilter")
(def ^:const web3-new-pending-transaction-filter "eth_newPendingTransactionFilter")
(def ^:const web3-new-block-filter "eth_newBlockFilter")
(def ^:const web3-uninstall-filter "eth_uninstallFilter")
(def ^:const web3-get-filter-changes "eth_getFilterChanges")

(def ^:const web3-shh-post "shh_post")
(def ^:const web3-shh-new-identity "shh_newIdentity")
(def ^:const web3-shh-has-identity "shh_hasIdentity")
(def ^:const web3-shh-new-group "shh_newGroup")
(def ^:const web3-shh-add-to-group "shh_addToGroup")
(def ^:const web3-shh-new-filter "shh_newFilter")
(def ^:const web3-shh-uninstall-filter "shh_uninstallFilter")
(def ^:const web3-shh-get-filter-changes "shh_getFilterChanges")
(def ^:const web3-shh-get-messages "shh_getMessages")

(defn web3-sign-message? [method]
  (#{web3-sign-typed-data web3-sign-typed-data-v3 web3-personal-sign} method))

(def ^:const status-create-address "status_createaddress")

; BIP44 Wallet Root Key, the extended key from which any wallet can be derived
(def ^:const path-wallet-root "m/44'/60'/0'/0")
; EIP1581 Root Key, the extended key from which any whisper key/encryption key can be derived
(def ^:const path-eip1581 "m/43'/60'/1581'")
; BIP44-0 Wallet key, the default wallet key
(def ^:const path-default-wallet (str path-wallet-root "/0"))
; EIP1581 Chat Key 0, the default whisper key
(def ^:const path-whisper (str path-eip1581 "/0'/0"))

(def ^:const path-default-wallet-keyword (keyword path-default-wallet))
(def ^:const path-whisper-keyword (keyword path-whisper))
(def ^:const path-wallet-root-keyword (keyword path-wallet-root))
(def ^:const path-eip1581-keyword (keyword path-eip1581))

;; (ethereum/sha3 "Transfer(address,address,uint256)")
(def ^:const event-transfer-hash "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef")

(def ^:const method-id-transfer "0xa9059cbb")
(def ^:const method-id-approve "0x095ea7b3")
(def ^:const method-id-approve-and-call "0xcae9ca51")

(def regx-emoji #"^((?:[\u261D\u26F9\u270A-\u270D]|\uD83C[\uDF85\uDFC2-\uDFC4\uDFC7\uDFCA-\uDFCC]|\uD83D[\uDC42\uDC43\uDC46-\uDC50\uDC66-\uDC69\uDC6E\uDC70-\uDC78\uDC7C\uDC81-\uDC83\uDC85-\uDC87\uDCAA\uDD74\uDD75\uDD7A\uDD90\uDD95\uDD96\uDE45-\uDE47\uDE4B-\uDE4F\uDEA3\uDEB4-\uDEB6\uDEC0\uDECC]|\uD83E[\uDD18-\uDD1C\uDD1E\uDD1F\uDD26\uDD30-\uDD39\uDD3D\uDD3E\uDDD1-\uDDDD])(?:\uD83C[\uDFFB-\uDFFF])?|(?:[\u231A\u231B\u23E9-\u23EC\u23F0\u23F3\u25FD\u25FE\u2614\u2615\u2648-\u2653\u267F\u2693\u26A1\u26AA\u26AB\u26BD\u26BE\u26C4\u26C5\u26CE\u26D4\u26EA\u26F2\u26F3\u26F5\u26FA\u26FD\u2705\u270A\u270B\u2728\u274C\u274E\u2753-\u2755\u2757\u2795-\u2797\u27B0\u27BF\u2B1B\u2B1C\u2B50\u2B55]|\uD83C[\uDC04\uDCCF\uDD8E\uDD91-\uDD9A\uDDE6-\uDDFF\uDE01\uDE1A\uDE2F\uDE32-\uDE36\uDE38-\uDE3A\uDE50\uDE51\uDF00-\uDF20\uDF2D-\uDF35\uDF37-\uDF7C\uDF7E-\uDF93\uDFA0-\uDFCA\uDFCF-\uDFD3\uDFE0-\uDFF0\uDFF4\uDFF8-\uDFFF]|\uD83D[\uDC00-\uDC3E\uDC40\uDC42-\uDCFC\uDCFF-\uDD3D\uDD4B-\uDD4E\uDD50-\uDD67\uDD7A\uDD95\uDD96\uDDA4\uDDFB-\uDE4F\uDE80-\uDEC5\uDECC\uDED0-\uDED2\uDEEB\uDEEC\uDEF4-\uDEF8]|\uD83E[\uDD10-\uDD3A\uDD3C-\uDD3E\uDD40-\uDD45\uDD47-\uDD4C\uDD50-\uDD6B\uDD80-\uDD97\uDDC0\uDDD0-\uDDE6])|(?:[#\*0-9\xA9\xAE\u203C\u2049\u2122\u2139\u2194-\u2199\u21A9\u21AA\u231A\u231B\u2328\u23CF\u23E9-\u23F3\u23F8-\u23FA\u24C2\u25AA\u25AB\u25B6\u25C0\u25FB-\u25FE\u2600-\u2604\u260E\u2611\u2614\u2615\u2618\u261D\u2620\u2622\u2623\u2626\u262A\u262E\u262F\u2638-\u263A\u2640\u2642\u2648-\u2653\u2660\u2663\u2665\u2666\u2668\u267B\u267F\u2692-\u2697\u2699\u269B\u269C\u26A0\u26A1\u26AA\u26AB\u26B0\u26B1\u26BD\u26BE\u26C4\u26C5\u26C8\u26CE\u26CF\u26D1\u26D3\u26D4\u26E9\u26EA\u26F0-\u26F5\u26F7-\u26FA\u26FD\u2702\u2705\u2708-\u270D\u270F\u2712\u2714\u2716\u271D\u2721\u2728\u2733\u2734\u2744\u2747\u274C\u274E\u2753-\u2755\u2757\u2763\u2764\u2795-\u2797\u27A1\u27B0\u27BF\u2934\u2935\u2B05-\u2B07\u2B1B\u2B1C\u2B50\u2B55\u3030\u303D\u3297\u3299]|\uD83C[\uDC04\uDCCF\uDD70\uDD71\uDD7E\uDD7F\uDD8E\uDD91-\uDD9A\uDDE6-\uDDFF\uDE01\uDE02\uDE1A\uDE2F\uDE32-\uDE3A\uDE50\uDE51\uDF00-\uDF21\uDF24-\uDF93\uDF96\uDF97\uDF99-\uDF9B\uDF9E-\uDFF0\uDFF3-\uDFF5\uDFF7-\uDFFF]|\uD83D[\uDC00-\uDCFD\uDCFF-\uDD3D\uDD49-\uDD4E\uDD50-\uDD67\uDD6F\uDD70\uDD73-\uDD7A\uDD87\uDD8A-\uDD8D\uDD90\uDD95\uDD96\uDDA4\uDDA5\uDDA8\uDDB1\uDDB2\uDDBC\uDDC2-\uDDC4\uDDD1-\uDDD3\uDDDC-\uDDDE\uDDE1\uDDE3\uDDE8\uDDEF\uDDF3\uDDFA-\uDE4F\uDE80-\uDEC5\uDECB-\uDED2\uDEE0-\uDEE5\uDEE9\uDEEB\uDEEC\uDEF0\uDEF3-\uDEF8]|\uD83E[\uDD10-\uDD3A\uDD3C-\uDD3E\uDD40-\uDD45\uDD47-\uDD4C\uDD50-\uDD6B\uDD80-\uDD97\uDDC0\uDDD0-\uDDE6])\uFE0F|[\t-\r \xA0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000\uFEFF])+$")
(def regx-rtl-characters #"[^\u0591-\u06EF\u06FA-\u07FF\u200F\u202B\u202E\uFB1D-\uFDFD\uFE70-\uFEFC]*?[\u0591-\u06EF\u06FA-\u07FF\u200F\u202B\u202E\uFB1D-\uFDFD\uFE70-\uFEFC]")
(def regx-url #"(?i)(?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9\-]+[.][a-z]{1,4}/?)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]){0,}")
(def regx-tag #"#[a-z0-9\-]+")
(def regx-mention #"@[a-z0-9\-]+")
(def regx-bold #"\*[^*]+\*")
(def regx-italic #"~[^~]+~")
(def regx-backquote #"`[^`]+`")
(def regx-universal-link #"((^https?://get.status.im/)|(^status-im://))[\x00-\x7F]+$")
(def regx-deep-link #"((^ethereum:.*)|(^status-im://[\x00-\x7F]+$))")

(def ^:const lines-collapse-threshold 20)
(def ^:const chars-collapse-threshold 600)
(def ^:const desktop-msg-chars-hard-limit 10000)

(def ^:const dapp-permission-contact-code "contact-code")
(def ^:const dapp-permission-web3 "web3")
(def ^:const dapp-permission-qr-code "qr-code")
(def ^:const api-response "api-response")
(def ^:const api-request "api-request")
(def ^:const history-state-changed "history-state-changed")
(def ^:const debug-metrics "debug_metrics")
(def ^:const web3-send-async "web3-send-async")
(def ^:const web3-send-async-read-only "web3-send-async-read-only")
(def ^:const web3-send-async-callback "web3-send-async-callback")
(def ^:const scan-qr-code "scan-qr-code")
(def ^:const scan-qr-code-callback "scan-qr-code-callback")

;;ipfs
(def ^:const ipfs-proto-code "e3")
(def ^:const swarm-proto-code "e4")
