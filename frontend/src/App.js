import { Layout, Input } from 'antd';
import IMenu from './components/IMenu';
import ITool from './components/ITool';
import React, { useState } from 'react';
import './App.css';

const { Header, Content, Sider, Footer } = Layout;
const { TextArea } = Input;

const App = () => {
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
          <ITool />
        </Sider>
        <Layout style={{ padding: '24px 24px 0px 24px' }}>
          <Content>
            <h2>摘要</h2>
            <TextArea
              value={ value }
              onChange={ e => setValue(e.target.value) }
              placeholder='二类水体主要包括内陆及近岸水体,受浮游植物、悬浮颗粒、有色可溶性有机物等多种因素影响,光学特性复杂多变,难以建立统一的水环境参数遥感定量估算模型。针对水体的光学特征,进行水体光学分类,进而反演水环境参数的方法,不仅能够提高参数估算精度,而且便于模型在同类水体中推广应用。水体光学分类方法主要包括基于固有光学特征的光学分类、基于遥感反射率波形特征的光学分类和以参数反演为目标的光学分类等方法。在分类反演的策略中,包括分类与模型算法融合、基于水体光学类型优选算法、优选多模型混合计算等方法。具体应用时,需要根据研究区水体光学特征的复杂程度和研究目的,选取不同的分类方法及参数遥感估算策略。'
              autoSize={{ minRows: 9, maxRows: 9 }}
              showCount={ true }
            />
            <h2 style={{ paddingTop: '24px' }}>标题</h2>
            <TextArea
              placeholder='基于水体光学分类的二类水体水环境参数遥感监测研究'
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
