(ns status-im.ui.components.tooltip.styles
  (:require [status-im.ui.components.colors :as colors]
            [status-im.utils.styles :as styles]))

(def tooltip-container
  {:position    :absolute
   :align-items :center
   :left        0
   :right       0
   :top         0})

(styles/def bottom-tooltip-container
  {:position    :absolute
   :align-items :center
   :left        12
   :right       12
   :ios         {:top 0}
   :android     {:top 30}})

(defn tooltip-animated [bottom-value opacity-value]
  {:position    :absolute
   :align-items :center
   :left        0
   :right       0
   :bottom      0
   :transform   [{:translateY bottom-value}]
   :opacity     opacity-value})

(defn tooltip-text-container [color]
  {:padding-horizontal 16
   :padding-vertical   9
   :background-color   color
   :elevation          2
   :border-radius      8})

(def bottom-tooltip-text-container
  {:flex-direction     :row
   :align-items        :center
   :margin-horizontal  12
   :padding-horizontal 16
   :padding-vertical   9
   :background-color   colors/gray
   :border-radius      8})

(defn tooltip-text [font-size]
  {:color     colors/red
   :font-size font-size})

(def bottom-tooltip-text
  {:color colors/white})

(def tooltip-triangle
  {:width  16
   :height 8})

(def close-icon
  {:margin-right 4
   :margin-left  10})
