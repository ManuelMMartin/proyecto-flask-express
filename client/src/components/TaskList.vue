<template>
  <div>
    <div className="col-12">
      <div className="card">
        <div className="card-header p-3">
          <h5>Tus tareas:</h5>
          <div v-if="tasks.length > 0">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Titulo</th>
                  <th scope="col">Descripcion</th>
                  <th scope="col">Prioridad</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="task in tasks" :class="{ 'table-success': task.completada }">
                  <th scope="row">{{ task.numero }}</th>
                  <td>{{ task.titulo }}</td>
                  <td>{{ task.descripcion }}</td>
                  <td>{{ task.prioridad }}</td>
                  <td>
                    <span v-if="!task.completada" @click='completar(task.numero)'>✔</span>
                    <span @click='eliminar(task.numero)'>🗑</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <h3>No tienes tareas, eres libre.</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div>
    <TaskForm :actualizar="actulizar" />
  </div>

</template>


<script>
import TaskForm from './TaskForm.vue';
import { URL } from '../assets/url';
export default {
  name: "TaskList",
  data() {
    return {
      mensaje: "",
      tasks: []
    };
  },
  mounted() {
    this.actulizar();
  },
  methods: {
    actulizar() {
      fetch(URL)
        .then(response => response.json())
        .then(data => {
          this.tasks = data.results;
        });
    },
    completar(task) {
      const requestOptions = {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          numero: task,
        })
      };
      fetch(`${URL}completar`, requestOptions)
        .then(response => response.json())
        .then(data => {
          this.actulizar();
          this.mensaje = data.mensaje;
        });
    },
    eliminar(task) {
      const requestOptions = {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          numero: task,
        })
      };
      fetch(`${URL}borrar`, requestOptions)
        .then(response => response.json())
        .then(data => {
          this.actulizar();
          this.mensaje = data.mensaje;
        });
    }
  },
  components: { TaskForm }
}
</script>

<style scoped>
span:hover {
  cursor: pointer;

}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
