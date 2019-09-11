(ns status-im.ui.screens.about-app.views
  (:require-macros [status-im.utils.views :as views])
  (:require [re-frame.core :as re-frame]
            [status-im.i18n :as i18n]
            [status-im.ui.components.colors :as colors]
            [status-im.ui.components.copyable-text :as copyable-text]
            [status-im.ui.components.icons.vector-icons :as vector-icons]
            [status-im.ui.components.list.views :as list]
            [status-im.ui.components.list-item.views :as list-item]
            [status-im.ui.components.react :as react]
            [status-im.ui.components.status-bar.view :as status-bar]
            [status-im.ui.components.toolbar.view :as toolbar]
            [status-im.ui.screens.about-app.styles :as styles]))

(defn- data [app-version node-version]
  [{:type                :small
    :title               (i18n/label :t/privacy-policy)
    :accessibility-label :privacy-policy
    :on-press
    #(re-frame/dispatch
      [:privacy-policy/privacy-policy-button-pressed])
    :accessories         [:chevron]}
   [copyable-text/copyable-text-view
    {:copied-text (str app-version "; " node-version)}
    [list-item/list-item
     {:type                :small
      :title               (i18n/label :t/version)
      :accessibility-label :version
      :accessories         [(str app-version ";\n" node-version)]}]]])

(views/defview about-app []
  (views/letsubs [app-version  [:get-app-short-version]
                  node-version [:get-app-node-version]]
    [react/view {:flex 1 :background-color colors/white}
     [status-bar/status-bar]
     [toolbar/simple-toolbar
      (i18n/label :t/about-app)]
     [list/flat-list
      {:data      (data app-version node-version)
       :key-fn    (fn [_ i] (str i))
       :render-fn list/flat-list-generic-render-fn}]]))

(views/defview learn-more-sheet []
  (views/letsubs [{:keys [title content]} [:bottom-sheet/options]]
    [react/view {:style {:padding-left 16 :padding-top 16
                         :padding-right 34 :padding-bottom 0}}
     [react/view {:style {:align-items :center :flex-direction :row :margin-bottom 16}}
      [vector-icons/icon :main-icons/info {:color colors/blue
                                           :container-style {:margin-right 13}}]
      [react/text {:style styles/learn-more-title} title]]
     [react/text {:style styles/learn-more-text} content]]))

(def learn-more
  {:content learn-more-sheet})
