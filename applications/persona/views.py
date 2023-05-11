from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  TemplateView,
                                  UpdateView,
                                  DeleteView)
# Models
from .models import Empleado
from django.urls import reverse_lazy
#forms
from .forms import EmpleadoForm
# Create your views here.
class InicioView(TemplateView):
    """Vista que carga la pagina de inicio"""
    template_name= 'inicio.html'


class ListaEmpleadosAdmin(ListView):
    template_name = 'persona/lista_empleados.html'
    ordering = 'first_name'
    paginate_by = 8
    context_object_name = 'all_empleados'
    model = Empleado


class ListAllEmpleados(ListView):
    template_name = 'persona/list_all.html'
    ordering = 'first_name'
    paginate_by = 4
    context_object_name = 'all_empleados'

    def get_queryset(self):
        # sourcery skip: inline-immediately-returned-variable
        palabra_clave = self.request.GET.get('kword', '')
        lista = Empleado.objects.filter(full_name__icontains=palabra_clave)
        return lista

class ListByAreaEmpleado(ListView):
    """Lista empleados de un area"""
    template_name = 'persona/list_by_area.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        # sourcery skip: inline-immediately-returned-variable
        # Override
        area = self.kwargs['shorname']
        lista = Empleado.objects.filter(departamento__shor_name=area)
        return lista

class ListByJobEmpleado(ListView):
    template_name = 'persona/list_by_job.html'

    def get_queryset(self):
        # Override
        job = self.kwargs['job']
        return Empleado.objects.filter(job=job)


class ListEmpleadosByKword(ListView):
    template_name = 'persona/by_kword.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        palabra_clave = self.request.GET.get('kword', '')
        return Empleado.objects.filter(first_name=palabra_clave)


class ListHabilidadesEmpleado(ListView):
    template_name = 'persona/habilidades.html'
    context_object_name = 'habilidades'

    def get_queryset(self):
        id_clave = int(self.request.GET.get('skills', ''))
        empleado = Empleado.objects.get(id=id_clave)
        return empleado.habilidad.all()


class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = 'persona/detail_empleado.html'

    def get_context_data(self, **kwargs):
        empleado = self.object
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs)
        context['titulo'] = f'{empleado.first_name} {empleado.last_name}'
        return context


class SuccessView(TemplateView):
    template_name = 'persona/success.html'


class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = 'persona/add.html'
    form_class = EmpleadoForm
    # fields = [
    #     'first_name',
    #     'last_name',    
    #     'job',
    #     'departamento',
    #     'habilidad',
    #     'avatar',
    # ]
    success_url = reverse_lazy('persona_app:empleado_all')

    def form_valid(self, form):
        # Logica del proceso
        empleado = form.save(commit=False)
        empleado.full_name = f'{empleado.first_name} {empleado.last_name}'
        empleado.save()
        return super(EmpleadoCreateView, self).form_valid(form)


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    template_name = 'persona/update.html'
    fields = [
        'first_name',
        'last_name',
        'job',
        'departamento',
        'habilidad'
    ]
    success_url = reverse_lazy('persona_app:empleados_admin')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('************POST************')
        print(request.POST)
        print(request.POST['last_name'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # Logica del proceso
        print('****************VALID*************')
        return super(EmpleadoUpdateView, self).form_valid(form)


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'persona/delete.html'
    success_url = reverse_lazy('persona_app:empleados_admin')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        try:
            return super(EmpleadoDeleteView, self).form_valid(form='POST')
        except ProtectedError:
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)

    def form_valid(self, form):
        empleado = self.object
        print(empleado.first_name)
        empleado.save()
        return super(EmpleadoDeleteView, self).form_valid(form)
