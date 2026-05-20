const { createApp } = Vue;

createApp({
    data() {
        return {
            showPage: 'home',
            loading: false,
            loadingResources: false,
            currentUser: null,

            // 用户表单数据
            formData: {
                name: '',
                grade: '',
                major: '',
                future_direction: '',
                weaknesses: '',
                interests: ''
            },

            // 规划数据
            planningData: null,

            // 资源数据
            resources: [],

            // 打卡表单
            checkInForm: {
                user_id: 1,
                check_in_date: new Date().toISOString().split('T')[0],
                task_completed: '',
                progress_notes: ''
            },

            // 打卡统计数据
            statistics: {
                total_days: 0,
                consecutive_days: 0,
                last_checkin_date: null,
                recent_records: []
            },

            // 打卡历史
            checkinRecords: [],

            // AI 聊天
            chatHistory: [],
            chatInput: '',
            messagesContainer: null,

            // 后台管理
            isAuthenticated: false,
            adminLogin: {
                username: '',
                password: ''
            },
            adminInfo: {},
            adminTab: 'templates',
            newTemplate: {
                major_name: '',
                core_courses: '',
                recommended_certificates: '',
                career_path: ''
            },
            newResource: {
                name: '',
                resource_type: 'course',
                target_major: '',
                target_direction: '',
                description: '',
                url: ''
            },
            templatesList: [],
            adminResourcesList: []
        };
    },

    mounted() {
        // 检查是否有缓存的用户信息
        const cachedUser = localStorage.getItem('currentUser');
        if (cachedUser) {
            this.currentUser = JSON.parse(cachedUser);
        }

        // 检查管理员状态（不再在挂载时调用 API，避免"未认证"错误）
        const cachedAdmin = localStorage.getItem('isAdmin');
        if (cachedAdmin === 'true') {
            this.isAuthenticated = true;
            this.adminInfo = { username: 'admin' };
            // loadTemplates 和 loadAdminResources 会在用户实际访问 admin 页面时调用
        }
    },

    methods: {
        // ==================== API 调用方法 ====================
        async apiCall(endpoint, options = {}) {
            try {
                const response = await fetch('/api' + endpoint, {
                    headers: {
                        'Content-Type': 'application/json',
                        ...(options.headers || {})
                    },
                    ...options
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail || data.message || '请求失败');
                }

                return data;
            } catch (error) {
                console.error('API 调用错误:', error);
                alert('请求失败：' + error.message);
                return null;
            }
        },

        // ==================== 页面导航 ====================
        changePage(page) {
            // 检查需要登录的页面
            const requireAuth = ['planning', 'resources', 'checkin', 'ai_chat'];
            if (requireAuth.includes(page) && !this.currentUser) {
                alert('请先完成用户注册！');
                this.showPage = 'register';
                return;
            }
            this.showPage = page;

            // 页面加载时的初始化操作
            if (page === 'planning' && this.currentUser) {
                this.loadPlanning();
            } else if (page === 'resources' && this.currentUser) {
                this.loadResources();
            } else if (page === 'checkin' && this.currentUser) {
                this.loadCheckinRecords();
                this.loadStatistics();
            } else if (page === 'ai_chat' && this.currentUser) {
                this.loadChatHistory();
            } else if (page === 'admin' && this.isAuthenticated) {
                this.loadTemplates();
                this.loadAdminResources();
            }
        },

        // ==================== 用户注册 ====================
        async submitRegistration() {
            if (!this.formData.name || !this.formData.grade || !this.formData.major || !this.formData.future_direction) {
                alert('请填写所有必填项！');
                return;
            }

            const result = await this.apiCall('/user/register', {
                method: 'POST',
                body: JSON.stringify(this.formData)
            });

            if (result) {
                this.currentUser = result;
                localStorage.setItem('currentUser', JSON.stringify(result));
                alert('注册成功！正在为您生成专属规划...');
                this.formData = {
                    name: '',
                    grade: '',
                    major: '',
                    future_direction: '',
                    weaknesses: '',
                    interests: ''
                };
                setTimeout(() => {
                    this.changePage('planning');
                }, 500);
            }
        },

        // ==================== 规划相关 ====================
        async loadPlanning() {
            this.loading = true;
            const result = await this.apiCall(`/planning/${this.currentUser.id}`);
            if (result) {
                this.planningData = result;
            }
            this.loading = false;
        },

        async generatePlanning() {
            this.loading = true;
            const result = await this.apiCall('/planning/generate', {
                method: 'POST',
                body: JSON.stringify({
                    user_id: this.currentUser.id,
                    generate_new: true
                })
            });

            if (result) {
                this.planningData = result;
                alert('规划生成成功！');
            }
            this.loading = false;
        },

        formatPlaintext(text) {
            return text.replace(/\n/g, '<br>');
        },

        // ==================== 资源相关 ====================
        async loadResources() {
            this.loadingResources = true;
            const params = new URLSearchParams({
                major: this.currentUser.major,
                direction: this.currentUser.future_direction
            }).toString();

            const result = await this.apiCall(`/resource/recommendations?${params}`);
            if (result) {
                this.resources = result;
            }
            this.loadingResources = false;
        },

        // ==================== 打卡相关 ====================
        async submitCheckIn() {
            if (!this.checkInForm.task_completed) {
                alert('请填写完成的任务！');
                return;
            }

            const result = await this.apiCall('/checkin/checkin', {
                method: 'POST',
                body: JSON.stringify({
                    user_id: this.currentUser.id,
                    check_in_date: this.checkInForm.check_in_date,
                    task_completed: this.checkInForm.task_completed,
                    progress_notes: this.checkInForm.progress_notes
                })
            });

            if (result) {
                alert('打卡成功！');
                this.checkInForm.task_completed = '';
                this.checkInForm.progress_notes = '';
                this.loadCheckinRecords();
                this.loadStatistics();
            }
        },

        async loadCheckinRecords() {
            const result = await this.apiCall(`/checkin/${this.currentUser.id}/records`);
            if (result) {
                this.checkinRecords = result;
            }
        },

        async loadStatistics() {
            const result = await this.apiCall(`/checkin/${this.currentUser.id}/statistics`);
            if (result) {
                this.statistics = result;
            }
        },

        // ==================== AI 问答相关 ====================
        async sendQuestion() {
            if (!this.chatInput.trim()) {
                return;
            }

            const userMessage = this.chatInput;
            this.chatHistory.push({ type: 'user', content: userMessage });
            this.chatInput = '';

            const result = await this.apiCall('/ai/ask', {
                method: 'POST',
                body: JSON.stringify({
                    user_id: this.currentUser.id,
                    question: userMessage
                })
            });

            if (result) {
                this.chatHistory.push({ type: 'ai', content: result.ai_answer });
            }

            this.$nextTick(() => {
                this.scrollToBottom();
            });
        },

        async loadChatHistory() {
            const result = await this.apiCall(`/ai/${this.currentUser.id}/history?limit=20`);
            if (result) {
                this.chatHistory = [];
                result.reverse().forEach(msg => {
                    this.chatHistory.push({ type: 'user', content: msg.user_question });
                    if (msg.ai_answer) {
                        this.chatHistory.push({ type: 'ai', content: msg.ai_answer });
                    }
                });
            }
            this.$nextTick(() => {
                this.scrollToBottom();
            });
        },

        scrollToBottom() {
            if (this.messagesContainer) {
                this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
            }
        },

        // ==================== 后台管理 ====================
        async adminLoginUser() {
            try {
                const response = await fetch('/api/admin/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: this.adminLogin.username,
                        password: this.adminLogin.password
                    })
                });

                const data = await response.json();

                if (data.token) {
                    this.isAuthenticated = true;
                    this.adminInfo = { username: this.adminLogin.username };
                    localStorage.setItem('isAdmin', 'true');
                    this.adminLogin = { username: '', password: '' };
                    this.loadTemplates();
                    this.loadAdminResources();
                    alert('登录成功！');
                } else {
                    alert('登录失败，请检查用户名和密码');
                }
            } catch (error) {
                alert('登录失败，请检查用户名和密码');
            }
        },

        logoutAdmin() {
            this.isAuthenticated = false;
            localStorage.setItem('isAdmin', 'false');
            this.adminTab = 'templates';
        },

        async loadTemplates() {
            const result = await this.apiCall('/admin/templates/list');
            if (result) {
                this.templatesList = result;
            }
        },

        async addTemplate() {
            if (!this.newTemplate.major_name) {
                alert('请填写专业名称！');
                return;
            }

            const result = await this.apiCall('/admin/templates/add', {
                method: 'POST',
                headers: {
                    'Authorization': 'Basic ' + btoa('admin:admin123'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.newTemplate)
            });

            if (result) {
                alert('模板添加成功！');
                this.newTemplate = {
                    major_name: '',
                    core_courses: '',
                    recommended_certificates: '',
                    career_path: ''
                };
                this.loadTemplates();
            }
        },

        async deleteTemplate(id) {
            if (!confirm('确定要删除这个模板吗？')) return;

            await this.apiCall(`/admin/templates/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Basic ' + btoa('admin:admin123')
                }
            });

            this.loadTemplates();
        },

        async loadAdminResources() {
            const result = await this.apiCall('/admin/resources/list');
            if (result) {
                this.adminResourcesList = result;
            }
        },

        async addResource() {
            if (!this.newResource.name) {
                alert('请填写资源名称！');
                return;
            }

            const result = await this.apiCall('/admin/resources/add', {
                method: 'POST',
                headers: {
                    'Authorization': 'Basic ' + btoa('admin:admin123'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.newResource)
            });

            if (result) {
                alert('资源添加成功！');
                this.newResource = {
                    name: '',
                    resource_type: 'course',
                    target_major: '',
                    target_direction: '',
                    description: '',
                    url: ''
                };
                this.loadAdminResources();
            }
        },

        async deleteResource(id) {
            if (!confirm('确定要删除这个资源吗？')) return;

            await this.apiCall(`/admin/resources/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Basic ' + btoa('admin:admin123')
                }
            });

            this.loadAdminResources();
        }
    }
}).mount('#app');
