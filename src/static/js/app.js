const vm = new Vue({
    el: '#orders',
    data: {
        orderItems: [],
        orderItemIds: [],
        totalPrice: 0
    },
    methods: {
        updateOrder: function(event) {
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
        }
    },
    delimiters: ['[[',']]']
})