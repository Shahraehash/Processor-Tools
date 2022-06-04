 <template>
    <apexchart type="bar" :options="options" :series="series"></apexchart> 
</template>
<script>
//packages
import _ from 'underscore'

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
      console.log(file.name)
      let item = {
        name: file.name, //not working
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
        xy = _.sortBy(xy, 'y').reverse()
        return xy
      },

  }
}
</script>
