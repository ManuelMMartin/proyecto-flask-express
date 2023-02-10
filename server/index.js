const express = require("express")
const app = express()
const cors = require("cors")
const port = process.env.PORT || 3000
//para que pueda leer lo que llega por body
app.use(express.urlencoded({ extended: false }))
app.use(express.json())
//para que pueda leer lo que llega por body
app.use(cors())
app.use(express.static('public'))
//Configuración mongodb
const mongodb = require('mongodb')
const MongoClient = mongodb.MongoClient

MongoClient.connect('mongodb://127.0.0.1:27017', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(client => {
  console.log('🟢MongoDB se ha conectado')
  app.locals.db = client.db("tasklist")
}).catch(err => console.error('🔴MongoDB no conectado. Error: ' + err))


app.get('/', (req, res) => {
  app.locals.db.collection("task").find().toArray((err, data) => {
    err
      ? res.send({ mensaje: "Error al acceder a la base de datos", results: err })
      : res.send({ mensaje: "Datos recuperados correctamente", results: data })
  })
});


app.post('/add', (req, res) => {
  if (req.body.numero === "" || req.body.titulo === "" || req.body.descripcion === "" || req.body.prioridad === "") {
    res.send({ mensaje: "Debes rellenar todos los campos" })
  } else if (req.body.numero <= 0) {
    res.send({ mensaje: "Debes indicar un numero positivo" })
  } else {
    app.locals.db.collection("task")
      .find({ numero: parseInt(req.body.numero) }).toArray((err, data) => {
        err
          ? res.send({ mensaje: "No se ha podido agregar la tarea", results: err })
          : data.length > 0
            ? res.send({ mensaje: `Ya existe una tarea con el numero: ${req.body.numero}`, results: data })
            : (app.locals.db.collection("task")
              .insertOne(
                {
                  numero: parseInt(req.body.numero),
                  titulo: req.body.titulo,
                  descripcion: req.body.descripcion,
                  prioridad: req.body.prioridad,
                  completada: false
                }, (err, data) => {
                  err
                    ? res.send({ mensaje: "No se ha podido agregar la tarea", results: err })
                    : res.send({ mensaje: "Agregada la tarea numero: " + req.body.numero, results: data })
                }))
      })
  }
})

app.put('/completar', (req, res) => {
  app.locals.db.collection('task').updateOne({ numero: parseInt(req.body.numero) },
    { $set: { completada: true } },
    (err, data) => {
      err
        ? res.send({ mensaje: "No se ha podido modificar la tarea", results: err })
        : res.send({ mensaje: `Tarea numero ${req.body.numero} completada!`, results: data })
    })
})

app.delete('/borrar', (req, res) => {
  app.locals.db.collection('task').deleteOne({ numero: parseInt(req.body.numero) }, (err, data) => {
    err
      ? res.send({ mensaje: "No se ha podido borrar la tarea", results: err })
      : res.send({ mensaje: `Borrada la tarea numero: ${req.body.numero}`, results: data })
  })
})


app.listen(port, err => {
  err
    ? console.log("🔴He fallado, lo siento")
    : console.log(`🟢estoy funcionando en localhost:${port}`)
})