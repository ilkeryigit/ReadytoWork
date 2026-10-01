import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import config
import i18n

TYPE_LABELS: dict = {}
BROWSER_LABELS: dict = {}
LANG_CODES = tuple(sorted(i18n.LANG_NAMES))


def refresh_labels(lang: str) -> None:
    TYPE_LABELS.clear()
    TYPE_LABELS.update({key: i18n.t(f"type.{key}", lang) for key in config.VALID_TYPES})
    BROWSER_LABELS.clear()
    BROWSER_LABELS.update(
        {key: i18n.t(f"browser.{key}", lang) for key in config.VALID_BROWSERS})


def commit(items, browser, lang, on_save, destroy, state) -> bool:
    """Save; close the window only when the write actually succeeded."""
    if not on_save(items, browser, lang):
        return False
    state["dirty"] = False
    destroy()
    return True


def _edit_dialog(parent, existing, items, refresh, mark_dirty):
    lang = i18n.get_lang()
    dialog = tk.Toplevel(parent)
    dialog.title(i18n.t("dialog.add_title" if existing is None else "dialog.edit_title", lang))
    dialog.transient(parent)
    dialog.grab_set()
    dialog.resizable(False, False)

    form = tk.Frame(dialog)
    form.pack(padx=12, pady=10)

    tk.Label(form, text=i18n.t("dialog.name", lang)).grid(row=0, column=0, sticky="w", pady=2)
    name_var = tk.StringVar(value=existing.name if existing else "")
    tk.Entry(form, textvariable=name_var, width=40).grid(row=0, column=1, pady=2)

    tk.Label(form, text=i18n.t("dialog.type", lang)).grid(row=1, column=0, sticky="w", pady=2)
    type_var = tk.StringVar(value=existing.type if existing else "program")
    ttk.Combobox(form, textvariable=type_var, values=list(TYPE_LABELS),
                 state="readonly", width=37).grid(row=1, column=1, pady=2)

    tk.Label(form, text=i18n.t("dialog.path", lang)).grid(row=2, column=0, sticky="nw", pady=2)
    path_var = tk.StringVar(value=existing.path if existing else "")
    tk.Entry(form, textvariable=path_var, width=40).grid(row=2, column=1, pady=2)

    browse_btn = tk.Button(form, text=i18n.t("dialog.browse", lang), command=lambda: _browse(dialog, type_var, path_var))
    browse_btn.grid(row=3, column=1, sticky="w", pady=2)

    def _browse_state(*_args):
        browse_btn.config(state="disabled" if type_var.get() == "url" else "normal")

    type_var.trace_add("write", _browse_state)
    _browse_state()

    buttons = tk.Frame(dialog)
    buttons.pack(fill="x", padx=12, pady=(0, 10))
    tk.Button(buttons, text=i18n.t("dialog.cancel", lang),
              command=dialog.destroy).pack(side="right", padx=3)
    tk.Button(buttons, text=i18n.t("dialog.ok", lang),
              command=_confirm).pack(side="right", padx=3)

    def _confirm():
        name = name_var.get().strip()
        path = path_var.get().strip()
        if not name or not path:
            return
        item = config.Item(name, type_var.get(), path)
        if existing is None:
            items.append(item)
        else:
            items[items.index(existing)] = item
        mark_dirty()
        refresh()
        dialog.destroy()


def _browse(dialog, type_var, path_var):
    if type_var.get() == "folder":
        chosen = filedialog.askdirectory(parent=dialog)
    elif type_var.get() != "url":
        chosen = filedialog.askopenfilename(parent=dialog)
    else:
        return
    if chosen:
        path_var.set(chosen)


def settings_window(items, browser, lang, on_save):
    i18n.set_lang(lang)
    refresh_labels(lang)

    root = tk.Tk()
    root.title(i18n.t("settings.title", lang))
    root.geometry("660x430")

    state = {"items": list(items), "dirty": False}
    buttons_by_key = {}

    lang_var = tk.StringVar(value=i18n.LANG_NAMES.get(lang, lang))
    browser_var = tk.StringVar(value=BROWSER_LABELS.get(browser, BROWSER_LABELS["default"]))

    top = tk.Frame(root)
    top.pack(fill="x", padx=8, pady=(8, 0))
    lang_label = tk.Label(top, text=i18n.t("settings.language", lang))
    lang_label.pack(side="left")
    lang_combo = ttk.Combobox(top, textvariable=lang_var, state="readonly", width=14,
                              values=[i18n.LANG_NAMES[code] for code in LANG_CODES])
    lang_combo.pack(side="left", padx=6)
    browser_label = tk.Label(top, text=i18n.t("settings.browser", lang))
    browser_label.pack(side="left", padx=(14, 0))
    browser_combo = ttk.Combobox(top, textvariable=browser_var, state="readonly", width=24,
                                 values=list(BROWSER_LABELS.values()))
    browser_combo.pack(side="left", padx=6)

    table = ttk.Treeview(root, columns=("name", "type", "path"), show="headings")
    table.heading("name", text=i18n.t("settings.column.name", lang))
    table.heading("type", text=i18n.t("settings.column.type", lang))
    table.heading("path", text=i18n.t("settings.column.path", lang))
    table.column("name", width=150)
    table.column("type", width=110)
    table.column("path", width=370)

    def _refresh():
        table.delete(*table.get_children())
        for item in state["items"]:
            table.insert("", "end", values=(
                item.name, TYPE_LABELS.get(item.type, item.type), item.path))

    def _selected_index():
        selection = table.selection()
        return table.index(selection[0]) if selection else None

    def _mark_dirty():
        state["dirty"] = True

    def _add():
        _edit_dialog(root, None, state["items"], _refresh, _mark_dirty)

    def _edit():
        index = _selected_index()
        if index is not None:
            _edit_dialog(root, state["items"][index], state["items"], _refresh, _mark_dirty)

    def _delete():
        index = _selected_index()
        if index is not None:
            del state["items"][index]
            _mark_dirty()
            _refresh()

    def _move(delta):
        index = _selected_index()
        if index is None:
            return
        target = index + delta
        if not 0 <= target < len(state["items"]):
            return
        state["items"][index], state["items"][target] = \
            state["items"][target], state["items"][index]
        _mark_dirty()
        _refresh()
        table.selection_set(table.get_children()[target])

    def _selected_browser():
        for code, label in BROWSER_LABELS.items():
            if label == browser_var.get():
                return code
        return "default"

    def _selected_lang():
        index = lang_combo.current()
        return LANG_CODES[index] if index >= 0 else lang

    def _save():
        commit(list(state["items"]), _selected_browser(), _selected_lang(),
               on_save, root.destroy, state)

    def _apply_language(*_args):
        new_lang = _selected_lang()
        i18n.set_lang(new_lang)
        refresh_labels(new_lang)
        root.title(i18n.t("settings.title", new_lang))
        lang_label.config(text=i18n.t("settings.language", new_lang))
        browser_label.config(text=i18n.t("settings.browser", new_lang))
        browser_combo.config(values=list(BROWSER_LABELS.values()))
        table.heading("name", text=i18n.t("settings.column.name", new_lang))
        table.heading("type", text=i18n.t("settings.column.type", new_lang))
        table.heading("path", text=i18n.t("settings.column.path", new_lang))
        for key, button in buttons_by_key.items():
            button.config(text=i18n.t(key, new_lang))
        _refresh()

    lang_combo.bind("<<ComboboxSelected>>", _apply_language)
    browser_combo.bind("<<ComboboxSelected>>", _mark_dirty)

    table.pack(fill="both", expand=True, padx=8, pady=(8, 4))

    middle = tk.Frame(root)
    middle.pack(fill="x", padx=8, pady=4)
    for key, command in (("settings.add", _add), ("settings.edit", _edit),
                         ("settings.delete", _delete),
                         ("settings.up", lambda: _move(-1)),
                         ("settings.down", lambda: _move(1))):
        button = tk.Button(middle, text=i18n.t(key, lang), command=command)
        button.pack(side="left", padx=3)
        buttons_by_key[key] = button

    bottom = tk.Frame(root)
    bottom.pack(fill="x", padx=8, pady=(4, 8))

    def _request_close():
        if not state["dirty"]:
            root.destroy()
            return
        current = i18n.get_lang()
        if messagebox.askyesno(i18n.t("confirm.unsaved_title", current),
                               i18n.t("confirm.unsaved", current), parent=root):
            _save()
        else:
            root.destroy()

    cancel_btn = tk.Button(bottom, text=i18n.t("settings.cancel", lang),
                           command=_request_close)
    cancel_btn.pack(side="right", padx=3)
    buttons_by_key["settings.cancel"] = cancel_btn
    save_btn = tk.Button(bottom, text=i18n.t("settings.save", lang), command=_save)
    save_btn.pack(side="right", padx=3)
    buttons_by_key["settings.save"] = save_btn

    root.protocol("WM_DELETE_WINDOW", _request_close)
    _refresh()
    root.mainloop()
    return root
