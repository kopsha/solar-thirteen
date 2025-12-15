import St from 'gi://St'
import Clutter from 'gi://Clutter'
import GObject from 'gi://GObject'
import * as Main from 'resource:///org/gnome/shell/ui/main.js'

let widget

export function enable() {
    // Container that will live on the desktop background layer
    widget = new St.Widget({
        style_class: 'desktop-square',
        layout_manager: new Clutter.BinLayout(),
        reactive: false,
        can_focus: false,
        track_hover: false,
    })

    // Centered label
    const label = new St.Label({
        text: 'Hey Solar 13',
        style_class: 'desktop-square-label',
        x_align: Clutter.ActorAlign.CENTER,
        y_align: Clutter.ActorAlign.CENTER,
    })

    widget.add_child(label)

    // Position the square (center of primary monitor)
    const monitor = Main.layoutManager.primaryMonitor
    const size = 200

    widget.set_size(size, size)
    widget.set_position(
        Math.floor(monitor.x + (monitor.width - size) / 2),
        Math.floor(monitor.y + (monitor.height - size) / 2)
    )

    // Add to background group so it stays on the desktop
    Main.layoutManager._backgroundGroup.add_child(widget)
}

export function disable() {
    if (widget) {
        widget.destroy()
        widget = null
    }
}
