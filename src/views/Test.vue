<template>
    <div>
        <d3HeatMap :heatMapXYVal="testData"/>
    </div>

</template>>


<script>
import d3HeatMap from '@/components/d3HeatMap.vue'

import * as d3 from 'd3'

export default {
    name: 'TestView',
    components: {
        d3HeatMap
    },
    data() {
        return {
            testData: null,

        }

    },
    mounted() {
        this.queryTestData().then((data) => {
            this.testData = data
            data
        })

    },
    methods: {
        queryTestData() {
            return d3.json('https://clynx.s3.amazonaws.com/milo/test_data.json').then(rawData => {
                    console.log(rawData)
                    let data = []
                    rawData.forEach(item => {
                        let obj = {}
                        obj['group'] = item.x
                        obj['variable'] = item.y
                        obj['value'] = item.val
                        data.push(obj)
                    })
                    return data
             })
        }

    }

}
</script>