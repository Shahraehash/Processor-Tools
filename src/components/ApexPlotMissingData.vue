 <template>
    <apexchart type="bar" :options="options" :series="series"></apexchart> 
</template>
<script>
//packages

//support code

//components


export default {
  name: 'ApexPlotMissingData',
  components: {

  },
  data() {
    return {
      options: {
        chart: {
          id: 'vuechart-example'
        },

      },
      series: [],


    }
  },
  props: [
    'files'

  ],
  watch: {

  },
  mounted() {
    this.files.forEach(file => {
      let item = {
        label: file.name,
        data: this.covertObjectToXY(file.params.nanByColumn)
      }
      this.series.push(item)
    })

  },  
  methods: {
      covertObjectToXY(obj) {
        let xy = []
        for (let key in obj) {
          xy.push({
            x: key,
            y: obj[key]
          })
        }
        return xy
      },

  }
}
</script>
