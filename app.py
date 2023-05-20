import os

from flask import flash, redirect, render_template, request, url_for
from flask_discord import requires_authorization
from flask_sqlalchemy import SQLAlchemy

from acc_manager import AccManager
from models.info import Info, db
from setup import *


# Creating various variables and class objects
app = create_app()
db = SQLAlchemy(app)
db.init_app(app)
discord_session = setup_discord(app)
account_manager = AccManager(app, discord_session)

with app.app_context():
    db.engine.execute(
        "CREATE TABLE IF NOT EXISTS info ("
        "email TEXT NOT NULL, "
        "username TEXT NOT NULL, "
        "id INTEGER NOT NULL UNIQUE, "
        "is_verified INTEGER NOT NULL, "
        "status INTEGER NOT NULL, "
        "PRIMARY KEY(id));"
    )


status_info = account_manager.status_info


@app.route("/")
def index():
    return render_template("index.html", authorized=discord_session.authorized)


@app.route("/login/")
def login():
    flash("You are successfully logged in!", "info")
    try:
        return discord_session.create_session()
    except:
        flash("Something went wrong when logging in.", "error")
        os._exit(1)


@app.route("/logout/")
def logout():
    discord_session.revoke()
    flash("You have successfully logged out", "info")
    return redirect(url_for(".index"))


@app.route("/account/")
def account():
    if not discord_session.authorized:
        return render_template("login.html")

    user = account_manager.get_current_user()

    id = user.get("id")
    name = user.get("name")
    email = user.get("email")
    avatar = user.get("avatar")
    is_verified = user.get("is_verified")

    status = account_manager.get_status(id)

    if account_manager.get_user_from_database(id=id):
        if status == 5:  # Status checker
            return "Your account is banned."
        elif status > 1 or status < -1:
            return "Invalid status."

        return render_template(
            "account.html",
            name=name,
            email=email,
            avatar=avatar,
            status=status,
            status_info=status_info,
        )
    elif account_manager.get_user_from_database(id=id) is None:
        if is_verified:
            new_status = 1
        else:
            new_status = 0

        info = Info(
            email=email,
            username=name,
            id=id,
            is_verified=is_verified,
            status=new_status,
        )
        db.session.add(info)
        db.session.commit()
        return render_template(
            "account.html",
            name=name,
            email=email,
            avatar=avatar,
            status=status,
            status_info=status_info,
        )


@app.route("/callback/")
def callback():
    try:
        data = discord_session.callback()
        return redirect(data.get("redirect", "/"))
    except Exception as exc:
        return str(exc)


# Page of the administrator panel
@app.route("/admin_dashboard/")
@requires_authorization
def admin_dashboard():
    if not account_manager.check_if_admin():
        return "You must have administrator rights to access this page."

    users = account_manager.get_users()
    # display the page of the administrator panel with user data
    return render_template("admin_dashboard.html", users=users, status_info=status_info)


# admin_dashboard pages


# Account editing page
@app.route("/admin_dashboard/edit/<int:user_id>/", methods=["GET", "POST"])
@requires_authorization
def edit_user_handler(user_id):
    try:
        user_db = account_manager.get_user_raw(user_id)
        if user_db is None:
            flash(f"User with ID {user_id} not found.", "error")
        if request.method == "POST":
            # Some checks that you may not use
            # referer = request.headers.get("Referer")
            # if not request.form and referer and "http://127.0.0.1:5000" in referer:
            #     return "Form is not valid."

            user_db.update_status(new_status=int(request.form["status"]))
            db.session.commit()

            flash("Done!", "info")
            return redirect("/admin_dashboard/")
        elif request.method == "GET":
            return render_template(
                "edit_user.html", user=user_db, status_info=status_info
            )
    except Exception as exc:
        db.session.rollback()
        return f"Error: {exc}", "error"


# Delete user acc from DB page
@app.route("/admin-dashboard/delete/<int:user_id>/", methods=["GET", "POST"])
@requires_authorization
def delete_user_handler(user_id):
    try:
        user_db = account_manager.get_user_raw(user_id)
        if user_db is None:
            flash(f"User with ID {user_id} not found.", "error")
        else:
            user_db.delete()
            flash(f"The user with ID {user_id} was deleted.", "info")
    except Exception as exc:
        db.session.rollback()
        return f"Error: {exc}", "error"

    return redirect(url_for(".admin_dashboard"))


# Ban user(set status to 5) page
@app.route("/admin-dashboard/ban/<int:user_id>/", methods=["GET", "POST"])
@requires_authorization
def ban_user_handler(user_id):
    try:
        user_db = account_manager.get_user_raw(user_id)
        if user_db is None:
            flash(f"User with ID {user_id} not found.", "error")
        else:
            user_db.ban_user()
            flash(f"The user with ID {user_id} was banned.", "info")
    except Exception as exc:
        db.session.rollback()
        return f"Error: {exc}", "error"

    return redirect(url_for(".admin_dashboard"))


# region errorhandlers
@app.errorhandler(404)
def page_not_found(error):
    return "Page not found, 404", 404


@app.errorhandler(400)
def bad_request(error):
    return "Incorrect request", 400


@app.errorhandler(403)
def forbidden(error):
    return "Access is denied", 403


@app.errorhandler(500)
def internal_server_error(error):
    return "Internal Server Error", 500


@app.errorhandler(502)
def bad_gateway(error):
    return "Bad gateway", 502


@app.errorhandler(503)
def service_unavailable(error):
    return "Service is unavailable", 503


# endregion errorhandler


if __name__ == "__main__":
    app.run(debug=True)
