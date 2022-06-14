import { Layout, Input } from 'antd';
import IMenu from './components/IMenu';
import ITool from './components/ITool';
import React, { useState } from 'react';
import './App.css';

const { Header, Content, Sider, Footer } = Layout;
const { TextArea } = Input;

const App = () => {
  const [title, setTitle] = useState('');
  const [collapsed, setCollapsed] = useState(true);
  const [value, setValue] = useState('');
  return (
    <Layout>
      <Header className='header'>
        <IMenu />
      </Header>
      <Layout>
        <Sider
          collapsible collapsed={ collapsed }
          onCollapse={ value => setCollapsed(value) }
          theme='light'
          className='site-layout-background'>
          <ITool abstract={ value } setTitle={ setTitle }/>
        </Sider>
        <Layout style={{ padding: '24px 24px 0px 24px' }}>
          <Content>
            <h2>摘要</h2>
            <TextArea
              value={ value }
              onChange={ e => setValue(e.target.value) }
              placeholder='请输入论文摘要'
              autoSize={{ minRows: 9, maxRows: 9 }}
              showCount={ true }
            />
            <h2 style={{ paddingTop: '24px' }}>标题</h2>
            <TextArea
              value={ title }
              placeholder='预测标题'
              autoSize={{ minRows: 9, maxRows: 9 }}
              showCount={ true }
              disabled={ true }
            />
          </Content>
          <Footer style={{ textAlign: 'center' }}>
            Abstract to title ©2022 Created by GEOYEE
          </Footer>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default App;
