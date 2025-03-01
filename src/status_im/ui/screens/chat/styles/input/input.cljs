(ns status-im.ui.screens.chat.styles.input.input
  (:require [status-im.ui.components.colors :as colors]
            [status-im.ui.screens.chat.styles.message.message :refer [message-author-name]]
            [status-im.utils.styles :as styles]))

(def min-input-height 36)
(def padding-vertical 8)
(def border-height 1)
(def max-input-height (* 5 min-input-height))

(defn root [margin-bottom]
  {:background-color colors/white
   :margin-bottom    margin-bottom
   :flex-direction   :column
   :border-top-width border-height
   :border-top-color colors/gray-lighter})

(def reply-message
  {:flex-direction :row
   :align-items    :flex-start
   :justify-content :space-between
   :padding-top    8
   :padding-bottom 8
   :padding-right  8
   :padding-left   8})

(def reply-message-content
  {:flex-direction :column
   :padding-left   8
   :padding-right 8
   :max-height     140})

(defn reply-message-author [chosen?]
  (assoc (message-author-name chosen?)
         :flex-shrink 1
         ;; NOTE:  overriding the values from the definition of message-author-name
         :padding-left 0
         :padding-top 0
         :padding-bottom 0
         :margin 0
         :height 18
         :include-font-padding false))

(def reply-message-container
  {:flex-direction :column-reverse})

(def reply-message-to-container
  {:flex-direction :row
   :height 18
   :padding-top 0
   :padding-bottom 0
   :padding-right 8
   :justify-content :flex-start})

(def reply-icon
  {:width 20
   :margin-top 1
   :margin-bottom 1
   :margin-right 0})

(def cancel-reply-highlight
  {:align-self :flex-start
   :width 19
   :height   19})

(def cancel-reply-container
  {:flex-direction  :row
   :justify-content :flex-end
   :height "100%"})

(def cancel-reply-icon
  {:background-color colors/gray
   :width 21
   :height 21
   :align-items :center
   :justify-content :center
   :border-radius    12})

(def input-container
  {:flex-direction   :row
   :align-items      :flex-end
   :padding-left     14})

(def input-root
  {:padding-top    padding-vertical
   :padding-bottom padding-vertical
   :flex           1})

(def input-animated
  {:align-items    :flex-start
   :flex-direction :row
   :flex-grow      1
   :min-height     min-input-height
   :max-height     max-input-height})

(styles/defn input-view [single-line-input?]
  {:flex           1
   :padding-top    9
   :padding-bottom 5
   :padding-right  12
   :min-height     min-input-height
   :max-height     (if single-line-input?
                     min-input-height
                     max-input-height)
   :android        {:padding-top 3}})

(def invisible-input-text
  {:position         :absolute
   :left             0
   :background-color :transparent
   :color            :transparent})

(styles/defn invisible-input-text-height [container-width]
  {:width            container-width
   :flex             1
   :padding-top      5
   :padding-bottom   5
   :android          {:padding-top 3}
   :position         :absolute
   :left             0
   :background-color :transparent
   :color            :transparent})

(styles/defn input-helper-view [left opacity]
  {:opacity  opacity
   :position :absolute
   :height   min-input-height
   :android  {:left (+ 4 left)}
   :ios      {:left left}
   :desktop  {:left left}})

(styles/defn input-helper-text [left]
  {:color               colors/gray
   :text-align-vertical :center
   :flex                1
   :android             {:top -1}
   :ios                 {:line-height min-input-height}
   :desktop             {:line-height min-input-height}})

(styles/defn seq-input-text [left container-width]
  {:min-width           (- container-width left)
   :position            :absolute
   :text-align-vertical :center
   :align-items         :center
   :android             {:left   (+ 2 left)
                         :height (+ 2 min-input-height)
                         :top    0.5}
   :ios                 {:line-height min-input-height
                         :height      min-input-height
                         :left        left}
   :desktop             {:line-height min-input-height
                         :height      min-input-height
                         :left        left}})

(def input-commands-icon
  {:margin        14
   :height        24
   :width         24})

(def input-clear-container
  {:width       24
   :height      24
   :margin-top  7
   :align-items :center})

(def commands-root
  {:flex-direction :row
   :align-items    :center})

(def command-list-icon-container
  {:width   32
   :height  32
   :padding 4})

(def commands-list-icon
  {:height 24
   :width  24})
