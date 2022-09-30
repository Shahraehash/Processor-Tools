<template>
    <div>
        {{stepNumber}}
        testComponent
        <v-btn @click="next">Next</v-btn>
        <v-btn @click="update">Update</v-btn>

    </div>
</template>
<script>
export default {
    name: 'testComponent',
    props: [
        'stepNumber',
        'stepTitle',
        'files'
    ],
    data() {
        return {
            test: 'test'
        }
    },
    methods: {
        next() {
            this.$emit('next', 'data')
        },
        update() {
            this.$emit('update', 'data')
        }
    }

}
</script>