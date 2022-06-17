 <template>
    <div>
        <v-data-table
            v-if="items != null"
            :headers="headers"
            :items="items"
        ></v-data-table>   
    </div>
 
</template>
<script>
//packages
import _ from 'underscore'

//support code

//components


export default {
  name: 'TableMissingDataByColumn',
  components: {

  },
  data() {
    return {
      headers: [
          {
            text: 'Column',
            align: 'start',
            sortable: false,
            value: 'column',
          },   
          {
            text: 'Count',
            align: 'start',
            sortable: false,
            value: 'count',
          }, 
          {
            text: 'Percent',
            align: 'start',
            sortable: false,
            value: 'percent',
          }, 
          {
            text: 'File',
            align: 'start',
            sortable: false,
            value: 'file',
          },                                      
      ],
      items: null
    }
  },
  props: [
    'files'

  ],
  watch: {

  },
  mounted() {
    this.items = []
    this.files.forEach(file => {
        for (let key in file.params.nanByColumn) {
            let item = {
                column: key,
                count: file.params.nanByColumn[key],
                percent: file.params.nanByColumnPercent[key],
                file: file.name
            }
            this.items.push(item)
        }
        this.items = _.sortBy(this.items, 'count').reverse()
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
