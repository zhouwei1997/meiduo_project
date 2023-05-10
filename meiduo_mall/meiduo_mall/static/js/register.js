//创建vue对象
let vm = new Vue({
    el: '#app', // 通过ID选择器找到绑定的HTML内容
    // 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
    data: {
        // v - model
        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: '',
        image_code_url: '',
        uuid: '',
        // v - show
        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,
        // error_message
        error_name_message: '',
        error_mobile_message: '',
    },
    mounted() {
        //生成图形验证码
        this.generate_image_code()
    },
    methods: {
        //生成图形验证码方法
        generate_image_code() {
            this.uuid = generateUUID();
            this.image_code_url = '/image_codes/' + this.uuid + '/';
        },
        // 校验用户名
        check_username() {
            // 用户名是5 - 20个字符，[a - zA - Z0 - 9_]
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_name = false;
            } else {
                this.error_name_message = '请输入5-15个字符的用户名';
                this.error_name = true;
            }
            // 判断用户名是否重复注册
            if (this.error_name == false) {
                let url = '/usernames/' + this.username + '/count/'
                axios.get(url, {
                    responseType: 'JSON'
                })
                    .then(response => {
                        if (response.dara.count == 1) {
                            //用户名存在
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response)
                    })
            }
        },
        // 校验密码
        check_password() {
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        // 校验二次密码
        check_password2() {
            if (this.password != this.password2) {
                this.error_password2 = true;
            } else {
                this.error_password2 = false;
            }
        },
        // 校验手机号
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }
        },
        // 校验是否勾选协议
        check_allow() {
            if (this.allow) {
                this.allow = true;
            } else {
                this.allow = false;
            }
        },
        // 监听表单提交事件
        on_submit() {
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();
            //在校验之后，注册数据中，只要存在错误，就禁止表单提交
            if (this.error_name == true || this.error_password == true || this.error_password == true || this.error_mobile == true || this.error_allow == true) {
                //禁止表单提交
                window.event.returnValue = false;
            }
        }
    }
})
