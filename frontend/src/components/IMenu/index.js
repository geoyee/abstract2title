import {
  HomeOutlined,
  SettingOutlined,
  QuestionCircleOutlined,
  GithubOutlined } from '@ant-design/icons';
import { Menu } from 'antd';
import React from 'react';
import './index.css'

function getItem(label, key, icon) {
  return {
    label,
    key,
    icon,
  };
}

const items = [
  getItem('首页', 'home', <HomeOutlined />),
  getItem('设置', 'setting', <SettingOutlined />),
  getItem('使用说明', 'readme', <QuestionCircleOutlined />),
  getItem('项目链接', 'github', <GithubOutlined />),
];  // submenu keys of first level

const IMenu = () => {
  return (
    <div>
      <div className='logo' />
      <h1 className='font'>论文标题生成系统</h1>
      <Menu
        className='ui'
        theme='dark'
        mode='horizontal'
        defaultSelectedKeys={['M1']}
        items={items} />
    </div>
  );
};

export default IMenu;
