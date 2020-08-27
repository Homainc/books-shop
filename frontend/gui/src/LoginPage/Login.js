import React from 'react';
import { Form, Input, Button, Checkbox, Spin   } from 'antd';
import * as actions from '../_store/actions/auth';
import {connect} from 'react-redux';
import { NavLink, Redirect } from 'react-router-dom';
import { LoadingOutlined }from '@ant-design/icons';


export const antIcon = <LoadingOutlined style={{ fontSize: 24 }} />

export const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};
export const tailLayout = {
  wrapperCol: {
    offset: 8,
    span: 16,
  },
};

export const withMyHook = (Component) =>{
  return function WrappedComponent(props) {
    const [form] = Form.useForm();
    return <Component {...props} form={form} />;
  }
}


class NormalLoginForm extends React.Component{
  onFinish = (value) => {
    this.props.onAuth(value.username, value.password);
  }

  render(){
      const {token, error, form, loading} = this.props;

      if (token !== null){
        return (<Redirect to='/' />)
      }

      let errorMessage = null;
      if (error) {
          errorMessage = (
              <p>{error.message}</p>
          );
      }
      
      return (
        <div>
          {errorMessage}
           {
             loading ?
             <Spin indicator={antIcon} />
             
            :
            <Form {...layout} form={form} onFinish={this.onFinish} >
              <Form.Item
                label="Имя пользователя"
                name="username"
                rules={[
                  {
                    required: true,
                    message: 'Пожалуйста введите ваше имя пользователя!',
                  },
                ]}
              >
                <Input />
              </Form.Item>
        
              <Form.Item
                  label="Пароль"
                  name="password"
                  rules={[
                    {
                      required: true,
                      message: 'Пожалуйста введите ваш пароль!',
                    },
                  ]}
                >
                <Input.Password />
                
              </Form.Item>
        
              <Form.Item {...tailLayout}  name="remember" valuePropName="checked">
                <Checkbox>Запомнить меня</Checkbox>
              </Form.Item>
        
              <Form.Item wrapperCol={{...tailLayout.wrapperCol}}>
                <Button type="primary" htmlType="submit" style={{marginRight: '10px'}}>
                  Войти
                </Button>

                <NavLink
                  to='/signup/'> Регистрация
              </NavLink>
              </Form.Item>
            </Form>
          }
        </div>
      );
    }
}

const wrappedForm = withMyHook(NormalLoginForm);

const mapStateToProps = (state) => {
    return {
        loading: state.auth.loading,
        error: state.auth.error,
        token: state.auth.token
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onAuth: (username, password) => dispatch(actions.authLogin(username, password))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(wrappedForm);