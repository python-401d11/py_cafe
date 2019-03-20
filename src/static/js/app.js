const vm = new Vue({
    el: '#orders',
    data: {
        orderItems: [],
        orderItemIds: [],
        totalPrice: 0
    },
    methods: {
        addToOrder: function(event) {
            const item_id = event.target.dataset.id;
            const item_name = event.target.dataset.name;
            const item_price = event.target.dataset.price;
            const item = {
                id: item_id,
                name: item_name,
                price: item_price
            }
            this.orderItems.push(item);
            this.orderItemIds.push(item_id)
            this.totalPrice += parseFloat(item_price);
            console.log('orderItems: ' + this.orderItems);
            console.log('orderItemIds: ' + this.orderItemIds);
        },
        removeFromOrder: function(event) {
            const item_id = event.target.dataset.id;
            i = this.orderItems.findIndex((element) => {
                return element.id === item_id;
            });
            console.log(i)
            this.orderItems.splice(i, 1);
            j = this.orderItemIds.indexOf(item_id);
            if (j > -1) this.orderItemIds.splice(j, 1);
            console.log('orderItems: ' + this.orderItems);
            console.log('orderItemIds: ' + this.orderItemIds);
        }
    },
    delimiters: ['[[',']]']
})
