import {
    CodeSandboxOutlined,
    DiffOutlined,
    CopyOutlined,
    DeleteOutlined,
    BoldOutlined,
    FontSizeOutlined,
    FontColorsOutlined} from '@ant-design/icons';
import { Menu } from 'antd';
import React, { useState } from 'react';
import './index.css'

function getItem(label, key, icon) {
    return {
        label,
        key,
        icon,
    };
}

const items = [
    getItem('标题推理', 'infer', <CodeSandboxOutlined />),
    getItem('粘贴摘要', 'paste', <DiffOutlined />),
    getItem('清除摘要', 'delet', <DeleteOutlined />),
    getItem('复制标题', 'copy', <CopyOutlined />),
    getItem('字体加粗', 'bold', <BoldOutlined />),
    getItem('调整大小', 'size', <FontSizeOutlined />),
    getItem('调整颜色', 'color', <FontColorsOutlined />),
];  // submenu keys of first level

const ITool = () => {
    const [current, setCurrent] = useState('infer');

    const onClick = (e) => {
        setCurrent(e.key);
        if (e.key === 'infer') {
            let postData = { 'abstract': '铁路应急测绘保障工作贯穿铁路突发事件的预防、应对、处置和恢复的全过程，是铁路应急保障体系的重要内容和基础性工作。铁路系统目前还没有建立铁路应急测绘保障体系，没有形成成熟可行的保障机制，存在着应急测绘预案不完善、地理信息资源储备不足、专业应急测绘保障队伍不健全、突发事件现场资料获取传输及处理不及时等问题。根据铁路应急测绘保障工作的特点，基于近年来相关应急测绘项目应用成果，分析了铁路应急测绘保障的现状和必要性，提出了铁路应急测绘保障体系建设的总体思路，包括铁路应急测绘装备及队伍建设、铁路应急测绘保障预案及工作机制建设、铁路应急测绘保障中心建设和铁路应急测绘保障技术体系建设等内容；并梳理了构建先进的现代铁路工程应急测绘保障技术体系需重点研究的关键性技术。通过建立健全铁路应急测绘保障体系，全面提升铁路行业的应急测绘保障服务能力。' };
            fetch('http://127.0.0.1:8080/predict', {
                method: 'POST',
                mode: 'cors',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: JSON.stringify(postData)
            }).then(function(response) {
                console.log(response);
            });
        };
    };

    return (
        <Menu
            mode='inline'
            style={{
                height: '100%',
                borderRight: 0,
            }}
            onClick={ onClick }
            items={ items }
            selectable={ false }
        />
    );
};

export default ITool;
