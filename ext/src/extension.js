import Clutter from 'gi://Clutter'
import GObject from 'gi://GObject';
import St from 'gi://St';

import {Extension, gettext as _} from 'resource:///org/gnome/shell/extensions/extension.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';

const Indicator = GObject.registerClass(
class Indicator extends PanelMenu.Button {
    _init() {
        super._init(0.0, _('My Shiny Indicator'));

        this.add_child(new St.Icon({
            icon_name: 'face-smile-symbolic',
            style_class: 'system-status-icon',
        }));

        let item = new PopupMenu.PopupMenuItem(_('Show Notification'));
        item.connect('activate', () => {
            Main.notify(_('Whatʼs up, folks?'));
        });
        this.menu.addMenuItem(item);
    }
});

export default class IndicatorExampleExtension extends Extension {
    enable() {
        this._indicator = new Indicator();
        Main.panel.addToStatusArea(this.uuid, this._indicator);

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

    disable() {
        this._indicator.destroy();
        this._indicator = null;
    }
}
