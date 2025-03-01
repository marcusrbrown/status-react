(ns status-im.log-level.core
  (:require [re-frame.core :as re-frame]
            [status-im.multiaccounts.update.core :as multiaccounts.update]
            [status-im.react-native.js-dependencies :as rn-dependencies]
            [status-im.node.core :as node]
            [status-im.i18n :as i18n]
            [status-im.utils.fx :as fx]))

(fx/defn save-log-level
  [{:keys [db now] :as cofx} log-level]
  (let [settings      (get-in db [:multiaccount :settings])
        new-settings  (if log-level
                        (assoc settings :log-level log-level)
                        (dissoc settings :log-level))]
    (fx/merge cofx
              (multiaccounts.update/update-settings new-settings {})
              (node/prepare-new-config {:on-success #(when (not= (node/get-log-level settings)
                                                                 (node/get-log-level new-settings))
                                                       (re-frame/dispatch [:logout]))}))))

(fx/defn show-change-log-level-confirmation
  [{:keys [db]} {:keys [name value] :as log-level}]
  {:ui/show-confirmation {:title               (i18n/label :t/close-app-title)
                          :content             (i18n/label :t/change-log-level
                                                           {:log-level name})
                          :confirm-button-text (i18n/label :t/close-app-button)
                          :on-accept           #(re-frame/dispatch [:log-level.ui/change-log-level-confirmed value])
                          :on-cancel           nil}})

(fx/defn show-logging-enabled-confirmation
  [{:keys [db]} enabled]
  {:ui/show-confirmation {:title               (i18n/label :t/close-app-title)
                          :content             (i18n/label :t/change-logging-enabled
                                                           {:enable (i18n/label (if enabled
                                                                                  :enable :disable))})
                          :confirm-button-text (i18n/label :t/close-app-button)
                          :on-accept           #(re-frame/dispatch [:log-level.ui/logging-enabled-confirmed enabled])
                          :on-cancel           nil}})

(fx/defn save-logging-enabled
  [{:keys [db] :as cofx}  enabled]
  (.setValue rn-dependencies/desktop-config "logging_enabled" enabled)
  (let [settings (get-in db [:multiaccount :settings])]
    (multiaccounts.update/update-settings (assoc-in cofx [:db :desktop/desktop :logging-enabled] enabled)
                                          (if enabled (assoc settings :log-level "INFO") (dissoc settings :log-level))
                                          {:success-event [:multiaccounts.update.callback/save-settings-success]})))
