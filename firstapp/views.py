from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
from .models import CustomUser, Friends_record, Expense_record, Group, Group_data, Group_expense_record

# Base view
def base_view(request):
    return render(request, "base.html", {})

# Signup view
def signupForm_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'User already exists. Please log in.')
        else:
            user = CustomUser.objects.create_user(username, email, password, phone_no=phone_no)
            if user:
                login(request, user)
                return redirect("dashboard1_view")
            else:
                messages.error(request, 'Failed to create user. Please try again.')

    return render(request, "signup.html")

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard1_view')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect("base_view")

# Dashboard view
@login_required
def dashboard1_view(request):
    users = CustomUser.objects.all().exclude(username=request.user)
    friend_list = Friends_record.objects.filter(uid=request.user)
    group_query_set = Group.objects.filter(uid=request.user)
    other_group_list = Group_data.objects.filter(mid=request.user)

    Total_balance = sum(friend.owe_amount for friend in friend_list)
    request.user.total_balance = Total_balance
    request.user.save()

    group_list = list(group_query_set)
    for group in other_group_list:
        temp = Group.objects.get(gname=group.gid.gname)
        if temp not in group_list:
            group_list.append(temp)

    expense_list = Expense_record.objects.filter(payer_uid=request.user)
    shared_user_expense_list = Expense_record.objects.filter(shared_uid=request.user)
    expense_list = (expense_list | shared_user_expense_list).order_by('-date_field', '-time_field')

    group_expense_list = Group_expense_record.objects.filter(gid__in=group_query_set).order_by('-date_field', '-time_field')

    context = {
        'users': users,
        'friend_list': friend_list,
        'group_list': group_list,
        'expense_list': expense_list,
        'group_expense_list': group_expense_list
    }

    if 'groupname' in request.GET:
        groupname = request.GET.get('groupname')
        group = Group.objects.get(gname=groupname)
        members_list = Group_data.objects.filter(gid=group).exclude(mid=request.user)

        relation_list = []
        internal_members_list = Group_data.objects.filter(gid=group).exclude(mid=request.user)
        for member in internal_members_list:
            x = CustomUser.objects.get(username=member.mid)
            temp = Friends_record.objects.get(f_uid=x.uid, uid=request.user)
            relation_list.append(temp)

        context.update({
            'groupname': groupname,
            'members_list': members_list,
            'relation_list': relation_list,
            'openModal': request.GET.get('openModal') == 'true'
        })

    return render(request, "dashboard1.html", context)

# Add friend view
@login_required
def add_friend(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            current_user = request.user
            friend_user = CustomUser.objects.get(username=username, email=email)

            if current_user == friend_user:
                messages.error(request, 'You cannot add yourself as a friend.')
                return redirect("dashboard1_view")

            Friends_record.objects.create(uid=current_user, f_uid=friend_user)
            messages.success(request, 'Friend added successfully!')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User with provided username and email does not exist.')
        except IntegrityError:
            messages.error(request, 'Friend already exists.')

    return redirect("dashboard1_view")

# Add group view
@login_required
def add_group(request):
    if request.method == "POST":
        gname = request.POST.get('groupname')
        try:
            group = Group(uid=request.user, gname=gname)
            group.save()
            Group_data.objects.create(gid=group, mid=request.user)
            messages.success(request, 'Group created successfully!')
        except IntegrityError:
            messages.error(request, 'Group name already exists.')
    return redirect("dashboard1_view")

# Add expense view
@login_required
def add_expense(request):
    if request.method == 'POST':
        friend = request.POST.get('friend_id')
        return render(request, 'add_expense_form.html', {'friend': friend})
    return HttpResponse("Invalid request method", status=405)

@login_required
def add_expense_form(request):
    if request.method == "POST":
        total_amount = request.POST.get('total_amount')
        s_uid = request.POST.get('friend_username')

        if not total_amount:
            return HttpResponse("Total amount is missing", status=400)

        try:
            shared_user = CustomUser.objects.get(username=s_uid)
        except CustomUser.DoesNotExist:
            return HttpResponse(f"User with username {s_uid} does not exist", status=400)

        splited_amount = float(total_amount) / 2
        description = request.POST.get('description')

        expense = Expense_record(
            payer_uid=request.user,
            shared_uid=shared_user,
            total_amount=total_amount,
            splited_amount=splited_amount,
            description=description
        )
        expense.save()

        friend_relation = Friends_record.objects.get(f_uid=shared_user.uid, uid=request.user)
        reverse_friend_relation = Friends_record.objects.get(f_uid=request.user.uid, uid=shared_user.uid)

        friend_relation.owe_amount += splited_amount
        reverse_friend_relation.owe_amount -= splited_amount

        friend_relation.save()
        reverse_friend_relation.save()

        return redirect("dashboard1_view")

    return render(request, 'add_expense_form.html')

# Settlement view
@login_required
def settlement_view(request):
    if request.method == "POST":
        s_uid = request.POST.get('friend_id')
        
        try:
            friend = CustomUser.objects.get(username=s_uid)
            friend_relation = Friends_record.objects.get(f_uid=friend, uid=request.user)
            reverse_friend_relation = Friends_record.objects.get(f_uid=request.user, uid=friend)

            friend_relation.owe_amount = 0
            reverse_friend_relation.owe_amount = 0

            friend_relation.save()
            reverse_friend_relation.save()

            Expense_record.objects.filter(shared_uid=friend).delete()
            
        except CustomUser.DoesNotExist:
            return HttpResponse(f"User with username {s_uid} does not exist", status=400)
        except Friends_record.DoesNotExist:
            return HttpResponse("Friend relationship does not exist", status=400)
        
        return redirect("dashboard1_view")
    
    return redirect("dashboard1_view")

# Group view
@login_required
def group_view(request):
    if request.method == 'POST':
        groupname = request.POST.get('groupname')
        group = Group.objects.get(gname=groupname)
        url = f"{reverse('dashboard1_view')}?groupname={groupname}&openModal=true"
        return redirect(url)

# Add group members view
@login_required
def add_group_members(request):
    gname = request.POST.get('groupname')
    
    if request.method == "POST":
        member_username = request.POST.get('selected_value')

        try:
            group = Group.objects.get(gname=gname)
            new_member = CustomUser.objects.get(username=member_username)
            
            if Group_data.objects.filter(gid=group, mid=new_member).exists():
                messages.error(request, "This user is already a member of the group.")
            else:
                Group_data.objects.create(gid=group, mid=new_member)

                members_list = Group_data.objects.filter(gid=group).exclude(mid=request.user).exclude(mid=new_member)
                for member in members_list:
                    friend_list = Friends_record.objects.filter(uid=member.mid)

                    def is_value_not_present(my_list, target_value):
                        return not any(obj.f_uid == target_value for obj in my_list)

                    if is_value_not_present(friend_list, new_member):
                        friend_user = CustomUser.objects.get(username=new_member)

                        Friends_record.objects.create(uid=member.mid, f_uid=friend_user)
                        Friends_record.objects.create(uid=friend_user, f_uid=member.mid)

        except Group.DoesNotExist:
            messages.error(request, "The specified group does not exist.")
        except CustomUser.DoesNotExist:
            messages.error(request, "The specified user does not exist.")
        except IntegrityError:
            messages.error(request, "There was an error adding the member to the group. Please try again.")
        
        url = f"{reverse('dashboard1_view')}?groupname={gname}&openModal=true"
        return redirect(url)

    return redirect("dashboard1_view")

# Add group expense record view
@login_required
def add_group_expense_record(request):
    if request.method == "POST":
        total_amount = request.POST.get('total_amount')
        description = request.POST.get('description')
        groupname = request.POST.get('groupname')

        group = get_object_or_404(Group, gname=groupname)
        group_members = Group_data.objects.filter(gid=group)
        member_count = group_members.count()   

        splited_amount = float(total_amount) / member_count

        expense = Group_expense_record(
            payer_uid=request.user,
            gid=group,
            total_amount=total_amount,
            splited_amount=splited_amount,
            description=description
        )
        expense.save()

        for member in group_members:
            temp = member.mid
            if temp != request.user:
                friend_relation = Friends_record.objects.get(f_uid=temp.uid, uid=request.user)
                reverse_friend_relation = Friends_record.objects.get(f_uid=request.user, uid=temp.uid)

                friend_relation.owe_amount += splited_amount
                reverse_friend_relation.owe_amount -= splited_amount

                friend_relation.save()
                reverse_friend_relation.save()

        url = f"{reverse('dashboard1_view')}?groupname={groupname}&openModal=true"
        return redirect(url)
    return redirect('dashboard1_view')

# Add expense separate view
@login_required
def add_expense_separate(request):
    if request.method == "POST":
        total_amount = float(request.POST.get('amount'))
        description = request.POST.get('description')
        selected_friends = request.POST.getlist('selected_items')

        if selected_friends:
            split_amount = total_amount / (len(selected_friends) + 1)

            expense = Expense_record(
                payer_uid=request.user,
                total_amount=total_amount,
                splited_amount=split_amount,
                description=description
            )
            expense.save()

            for friend_username in selected_friends:
                friend_user = CustomUser.objects.get(username=friend_username)

                friend_relation, created = Friends_record.objects.get_or_create(
                    f_uid=friend_user, uid=request.user,
                    defaults={'owe_amount': 0}
                )
                reverse_friend_relation, created = Friends_record.objects.get_or_create(
                    f_uid=request.user, uid=friend_user,
                    defaults={'owe_amount': 0}
                )

                friend_relation.owe_amount += split_amount
                reverse_friend_relation.owe_amount -= split_amount

                friend_relation.save()
                reverse_friend_relation.save()

            messages.success(request, 'Expense added and split successfully!')
        else:
            messages.error(request, 'No friends selected for splitting the expense.')

    return redirect('dashboard1_view')


# group settlement view
@login_required
def group_settlement_view(request):
    if request.method == "POST":
        groupname = request.POST.get('groupname')
        
        try:
            group = get_object_or_404(Group, gname=groupname)
            Group_expense_record.objects.filter(gid=group).delete()
            messages.success(request, 'All group expenses have been settled.')
        except Group.DoesNotExist:
            messages.error(request, 'Group does not exist.')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
        
        return redirect("dashboard1_view")
    
    return redirect("dashboard1_view")


# Clear all records where the current user is either the payer or the shared user and total_amount != splited_amount
from django.db.models import Q, F

@login_required
def clear_records(request):
    if request.method == "POST":
        try:
            # Fetch Expense_records where the current user is either payer or shared user and total_amount != splited_amount
            expenses_to_clear = Expense_record.objects.filter(
                Q(payer_uid=request.user) | Q(shared_uid=request.user),
                ~Q(total_amount=F('splited_amount'))
            )
            
            # Delete the fetched records
            deleted_count, _ = expenses_to_clear.delete()
            
            # Inform the user about the number of records deleted
            messages.success(request, f'{deleted_count} expense records were successfully cleared.')
        except Exception as e:
            # Handle any exceptions and inform the user
            messages.error(request, f'An error occurred: {e}')
        
        return redirect("dashboard1_view")
    
    return redirect("dashboard1_view")