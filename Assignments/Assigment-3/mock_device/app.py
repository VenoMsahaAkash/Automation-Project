from flask import (
    Flask,
    request,
    redirect,
    url_for,
    session,
    render_template_string
)


app = Flask(__name__)

app.secret_key = "embedded-device-secret"


# ==========================================================
# DEVICE DATA
# ==========================================================

DEVICE = {

    "name": "QEMU-Embedded-Device",

    "status": "ONLINE",

    "mode": "NORMAL",

    "feature_enabled": False
}


# ==========================================================
# LOGIN PAGE
# ==========================================================

LOGIN_HTML = """

<!DOCTYPE html>

<html>

<head>

    <title>Device Login</title>

</head>

<body>

    <h1>
        Embedded Device Login
    </h1>


    <form method="post">

        <label>
            Username:
        </label>

        <input
            id="username"
            name="username"
            type="text"
        >


        <br>
        <br>


        <label>
            Password:
        </label>

        <input
            id="password"
            name="password"
            type="password"
        >


        <br>
        <br>


        <button
            id="login-button"
            type="submit"
        >
            Login
        </button>

    </form>


    {% if error %}

        <p id="error">
            {{ error }}
        </p>

    {% endif %}

</body>

</html>

"""


# ==========================================================
# DASHBOARD PAGE
# ==========================================================

DASHBOARD_HTML = """

<!DOCTYPE html>

<html>

<head>

    <title>
        Embedded Device Dashboard
    </title>

</head>


<body>


<h1 id="dashboard-title">

    Embedded Device Dashboard

</h1>


<p id="device-name">

    Device: {{ device.name }}

</p>


<p id="device-status">

    Status: {{ device.status }}

</p>


<p id="device-mode">

    Mode: {{ device.mode }}

</p>


<p id="feature-status">

    Feature:

    {% if device.feature_enabled %}

        ENABLED

    {% else %}

        DISABLED

    {% endif %}

</p>


<!-- DEVICE MODE -->

<form
    method="post"
    action="{{ url_for('set_mode') }}"
>


<select
    id="mode"
    name="mode"
>

    <option value="NORMAL">

        NORMAL

    </option>


    <option value="POWER_SAVE">

        POWER_SAVE

    </option>


    <option value="MAINTENANCE">

        MAINTENANCE

    </option>

</select>


<button
    id="apply-mode"
    type="submit"
>

    Apply Mode

</button>


</form>


<br>


<!-- FEATURE -->

<form
    method="post"
    action="{{ url_for('toggle_feature') }}"
>


<button
    id="feature-button"
    type="submit"
>

    {% if device.feature_enabled %}

        Disable Feature

    {% else %}

        Enable Feature

    {% endif %}

</button>


</form>


<br>


<!-- LOGOUT -->

<a
    id="logout"
    href="{{ url_for('logout') }}"
>

    Logout

</a>


</body>

</html>

"""


# ==========================================================
# LOGIN ROUTE
# ==========================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)

def login():

    if "user" in session:

        return redirect(
            url_for("dashboard")
        )


    error = None


    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )


        if (
            username == "admin"
            and
            password == "admin123"
        ):

            session["user"] = "admin"

            return redirect(
                url_for("dashboard")
            )


        error = (
            "Invalid username or password"
        )


    return render_template_string(
        LOGIN_HTML,
        error=error
    )


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")

def dashboard():

    if "user" not in session:

        return redirect(
            url_for("login")
        )


    return render_template_string(
        DASHBOARD_HTML,
        device=DEVICE
    )


# ==========================================================
# CHANGE DEVICE MODE
# ==========================================================

@app.post("/set-mode")

def set_mode():

    if "user" not in session:

        return redirect(
            url_for("login")
        )


    mode = request.form.get(
        "mode"
    )


    allowed_modes = [

        "NORMAL",

        "POWER_SAVE",

        "MAINTENANCE"

    ]


    if mode in allowed_modes:

        DEVICE["mode"] = mode


    return redirect(
        url_for("dashboard")
    )


# ==========================================================
# TOGGLE FEATURE
# ==========================================================

@app.post("/toggle-feature")

def toggle_feature():

    if "user" not in session:

        return redirect(
            url_for("login")
        )


    DEVICE["feature_enabled"] = (
        not DEVICE["feature_enabled"]
    )


    return redirect(
        url_for("dashboard")
    )


# ==========================================================
# LOGOUT
# ==========================================================

@app.get("/logout")

def logout():

    session.clear()


    return redirect(
        url_for("login")
    )


# ==========================================================
# START APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )