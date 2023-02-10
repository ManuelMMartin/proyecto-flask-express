<template>
  <h2>Agrega Tareas a tu lista</h2>
  <div class="task-form">
    <form @submit.prevent="enviarFormulario">
      <div class="container">
        <div class="row">
          <div class="col-2">
            <div class="form-group">
              <label>Numero</label>
              <input min="1" type="number" class="form-control" v-model="task.numero" ref="numero"
                :class="{ 'is-invalid': procesando && validoNumero }" @focus="resetEstado" @keypress="resetEstado">
            </div>
          </div>
          <div class="col-5">
            <div class="form-group">
              <label>Prioridad</label>
              <select v-model="task.prioridad" class="form-select" ref="prioridad"
                :class="{ 'is-invalid': procesando && validoPrioridad }" @focus="resetEstado" @keypress="resetEstado">
                <option value="Normal">Normal</option>
                <option value="Urgente">Urgente</option>
              </select>
            </div>
          </div>
          <div class="col-5">
            <div class="form-group">
              <label>Titulo</label>
              <input type="text" class="form-control" v-model="task.titulo" ref="titulo"
                :class="{ 'is-invalid': procesando && validoTitulo }" @focus="resetEstado" @keypress="resetEstado">
            </div>
          </div>
          <div class="col-12">
            <div class="form-group">
              <label>descripcion</label>
              <input type="text" class="form-control" v-model="task.descripcion" ref="descripcion"
                :class="{ 'is-invalid': procesando && validoDescripcion }" @focus="resetEstado" @keypress="resetEstado">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <div class="form-group">
              <button @click="validoTarea" class="btn btn-primary mt-2 mb-2">Añadir tarea</button>
            </div>
          </div>
        </div>
      </div>
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <div v-if="error & procesando" class="alert alert-danger" role="alert">
              {{ mensaje }}
            </div>
            <div v-if="correcto" class="alert" :class="validoMensaje" role="alert">
              {{ mensaje }}
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { URL } from '../assets/url';
export default {
  name: 'TaskForm',
  props: {
    actualizar: Function
  },
  data() {
    return {
      procesando: false,
      error: false,
      correcto: false,
      mensaje: '',
      task: {
        numero: '',
        titulo: '',
        descripcion: '',
        prioridad: '',
      }
    }
  },
  methods: {

    enviarFormulario() {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          numero: this.$data.task.numero,
          titulo: this.$data.task.titulo,
          descripcion: this.$data.task.descripcion,
          prioridad: this.$data.task.prioridad
        })
      }

      fetch(`${URL}add`, requestOptions)
        .then(response => response.json())
        .then(data => {
          if (data.mensaje.includes('Agregada')) {
            this.actualizar()
            this.error = false
            this.correcto = true
            setTimeout(() => this.correcto = false, 3000)
            this.procesando = false
            this.task = {
              numero: '',
              titulo: '',
              descripcion: '',
              prioridad: ''
            }
          }

          this.mensaje = data.mensaje
        })

      this.procesando = true
      this.resetEstado()
      if (this.validoNumero || this.validoTitulo || this.validoDescripcion || this.validoPrioridad) {
        this.error = true
        return
      }
      this.$emit('add-task', this.task)
      this.error = false
      this.correcto = true
      this.procesando = false
    },
    resetEstado() {
      this.error = false
      this.correcto = false
    },
  },

  computed: {
    validoNumero() {
      return this.task.numero <= 0
    },
    validoTitulo() {
      return this.task.titulo.length < 1
    },
    validoDescripcion() {
      return this.task.descripcion.length < 1
    },
    validoPrioridad() {
      return this.task.prioridad.length < 1
    },
    validoMensaje() {
      return this.mensaje.includes('Agregada') ? 'alert-success' : 'alert-danger'
    }
  }
}


</script>

<style scoped>

</style>