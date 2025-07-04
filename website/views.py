from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from .models.parent import Parent
from .models.child import Child
from .models.transaction import Transaction
from .models.goal import Goal
from .models.chore import Chore
from datetime import date, datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        child_id = request.form['child_id']
        return redirect(url_for('views.view_child', child_id=child_id))
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/view-child', methods=['POST', 'GET'])
def view_child(child_id=None):  
    user = current_user
    if child_id is not None:
        user = Child.get
    if current_user.parentAccess:
        user = user.getChildren()[0]
    return render_template("view_child.html", child=user, user=current_user)

@views.route("/manage-child/<int:child_id>", methods=["GET", "POST"])
@login_required
def manage_child(child_id):
    child = Child.query.get_or_404(child_id)
    return render_template("manage_child.html", child=child, user=current_user)


@views.route("/add-chore/<int:child_id>", methods=["POST"])
def add_chore(child_id):
    child = Child.query.get_or_404(child_id)

    name = request.form.get("chore_name")
    description = request.form.get("chore_description")
    value = int(request.form.get("chore_value"))
    recurring = request.form.get("recurring")

    # Assume Chore constructor supports these fields
    chore = Chore(name=name, description=description, value=value, recurring=recurring)
    child.chores.append(chore)

    db.session.add(chore)
    db.session.commit()

    flash("Chore added successfully!", "success")
    return redirect(url_for("views.manage_child", child_id=child_id, user=current_user))

@views.route("/add-goal/<int:child_id>", methods=["POST"])
def add_goal(child_id):
    child = Child.query.get_or_404(child_id)

    name = request.form.get("goal_name")
    value = int(request.form.get("goal_value"))
    due_date = request.form.get("goal_due")
    description = request.form.get("goal_description")

    goal = Goal(name=name, value=value)
    if due_date:
        goal.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    if description:
        goal.description = description

    child.goals.append(goal)

    db.session.add(goal)
    db.session.commit()

    flash("Goal added successfully!", "success")
    return redirect(url_for("views.manage_child", child_id=child_id, user=current_user))

@views.route("/add-transaction/<int:child_id>", methods=["POST"])
def add_transaction(child_id):
    child = Child.query.get_or_404(child_id)

    value = int(request.form.get("transaction_value"))
    description = request.form.get("transaction_description")
    date_str = request.form.get("transaction_date")

    if date_str:
        transaction = Transaction(value=value, description=description, day=datetime.strptime(date_str, "%Y-%m-%d").date())
    else:
        transaction = Transaction(value=value, description=description)

    child.transactions.append(transaction)
    child.balance += value

    db.session.add(transaction)
    db.session.commit()

    flash("Transaction added successfully!", "success")
    return redirect(url_for("views.manage_child", child_id=child_id, user=current_user))


@views.route('/edit_chore/<int:chore_id>', methods=['GET', 'POST'])
def edit_chore(chore_id):
    chore = Chore.query.get_or_404(chore_id)
    if request.method == 'POST':
        chore.name = request.form['name']
        chore.description = request.form['description']
        chore.value = int(request.form['value'])
        chore.recurring = request.form['recurrence_type']
        db.session.commit()
        flash('Chore updated successfully!', 'success')
        return redirect(url_for('views.view_child', child_id=chore.child_id))
    return render_template('edit_chore.html', chore=chore, user=current_user)


@views.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if request.method == 'POST':
        transaction.description = request.form['description']
        transaction.changeValue(int(request.form['value']))
        # You may want to parse and update the date if applicable
        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('views.view_child', child_id=transaction.child_id))
    return render_template('edit_transaction.html', transaction=transaction, user=current_user)


@views.route('/edit_goal/<int:goal_id>', methods=['GET', 'POST'])
def edit_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if request.method == 'POST':
        goal.name = request.form['name']
        goal.value = int(request.form['value'])
        goal.description = request.form['description']
        # If you track due date, parse and update here
        db.session.commit()
        flash('Goal updated successfully!', 'success')
        return redirect(url_for('views.view_child', child_id=goal.child_id))
    return render_template('edit_goal.html', goal=goal, user=current_user)