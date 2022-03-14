from django.shortcuts import redirect, render

from attendance.models import Attendance
from .forms import CreateAttendanceForm

# Create your views here.
def create_attendance(request):
    form = CreateAttendanceForm()
    if request.POST:
        form = CreateAttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.manager = request.user
            attendance.save()
            return redirect('attendance:list')
    return render(request, 'attendance/create.html', {'form': form})

def list_attendance(request):
    if request.user.is_manager:
        attendances = Attendance.objects.filter(manager=request.user)
    else:
        attendances = Attendance.objects.filter(employee__user=request.user)
    print(Attendance.objects.all())
    return render(request, 'attendance/list.html', {'attendances': attendances})


def delete_attendance(request, pk):
    attendance = Attendance.objects.get(id=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('attendance:list')
    context = {'attendance': attendance}
    return render(request, 'attendance/delete.html', context=context)

def mark_attendance(request, id):
    attendance = Attendance.objects.get(id=id)
    attendance.marked = True
    attendance.save()
    return redirect('attendance:list')