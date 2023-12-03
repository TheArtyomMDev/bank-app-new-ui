from passcode.passcodewindow import PasscodeWidget


def passcode_setup(f):
    def decorator(*args, **kwargs):
        def on_passcode_entered(passcode):
            w.destroy()
            f(passcode=passcode, *args, **kwargs)

        w = PasscodeWidget("Enter new passcode", on_passcode_entered)
        w.show()

    return decorator


def passcode_required(f):
    def decorator(*args, **kwargs):
        def on_passcode_entered(passcode):
            w.destroy()
            f(passcode=passcode, *args, **kwargs)

        w = PasscodeWidget("Confirmation required", on_passcode_entered)
        w.show()

    return decorator
